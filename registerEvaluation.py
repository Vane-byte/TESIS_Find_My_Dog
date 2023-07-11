from difflib import SequenceMatcher
import re
import datetime
from datetime import datetime as dt
from datetime import date
import base64
from werkzeug.utils import secure_filename

point_weights={'NER':0.4, 'Image':0.6, 'ACC':6, 'COL':12,'DAT':9,'DOG':15,'HRS':3,'PEL':12,'PLC':12,'RAZ':15,'SEX':9,'STT':6,'TAM':12}

def obtener_porcentaje_similitud(frase1, frase2):
    matcher = SequenceMatcher(None, frase1, frase2)
    porcentaje_similitud = matcher.ratio()
    return porcentaje_similitud

def transformDate(dat):
  try:
    dat=dat.lower()
    today= date.today()
    dat= dat.replace('?','e').replace('?','a').replace('  ',' ')
    words= dat.split(' ')

    numsInDate= [int(s) for s in re.findall(r'-?\d+\.?\d*', dat)]
    homologationDays=["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]


    if 'hoy' in dat:
      dat= date.today()

    elif 'ayer' in dat:
      dat= today-datetime.timedelta(days=1)

    elif 'hace' in dat:
      dat=dat.replace('?','i')
      if 'dia' in dat:
        number=[1]
        if 'dias' in dat:
          number=[3]
          if len(numsInDate)>0:
            number = numsInDate
        dat=today-datetime.timedelta(days=number[0])

      elif 'semana' in dat:
        week=7
        number=[1]
        if len(numsInDate)>0:
          number = numsInDate
        dat= today-datetime.timedelta(days=week*number[0])
    elif ('pasado' in dat and len(numsInDate)==0) or (len(numsInDate)==0 and len(words)<=2):
      day=0
      for index,val in enumerate(homologationDays):
        if val in dat:
          day=index
          break
      todayDay=today.weekday() #4
      if todayDay<day:
        todayDay= todayDay+7
      daysPassed= todayDay-day
      dat= today- datetime.timedelta(days=daysPassed)
    else:
      dat = dat.lower().replace('.','-').replace('/','-').replace('--','-')
      dat.strip('.')
      if dat.count('-')==2 and len(numsInDate)==3:   #  28-02-23
        year=numsInDate[2]
        if year>9 and year<100:
          year='20'+str(year)
        dat=str(numsInDate[0])+'-'+str(numsInDate[1])+'-'+str(year)
        dat=dt.strptime(dat, '%d-%m-%Y').date()

      elif len(numsInDate)==2 and dat.count('-')==1:    #  28-02
        newDate= str(numsInDate[0])+"-"+str(numsInDate[1])+"-"+"2023"
        dat=dt.strptime(newDate, '%d-%m-%Y').date()

      else:
        homologationMonths={
            "01":['enero','ene'],
            "02":['feb','febrero'],
            "03":['mar','marzo'],
            "04":['abr','abril','april'],
            "05":['may','mayo'],
            "06":['jun','junio'],
            "07":['jul','julio'],
            "08":['ago','agosto'],
            "09":['set','sept','sep','setiembre','septiembre'],
            "10":['oct','octubre'],
            "11":['nov','noviembre'],
            "12":['dec','diciembre','dic']
        }

        # 7 de enero o 7 de enero 2023
        month= today.month
        day= today.day
        year= today.year
        for monthKey in homologationMonths:
          for monthVal in homologationMonths[monthKey]:
            if monthVal in dat:
              month=monthKey
              break
        day= numsInDate[0]
        if len(numsInDate) ==2: #tenemos d?a y a?o
          year= numsInDate[1]
          if year>9 and year <100:
            year='20'+str(year)

        newDate=str(day)+'-'+str(month)+'-'+str(year)
        dat= dt.strptime(newDate, '%d-%m-%Y').date()
    return dat
  except:
    return -1

def CalcNERPoints (NER_registro, NER_compare):
  points=0

  #ACC - placa, chip, collar
  def ACC_punctuation(acc1, acc2):
    contains_no = 'no' in acc1 and 'no' in acc2
    not_contains_no = not 'no' in acc1 and 'no' in acc2

    calc=0

    if contains_no or not_contains_no:
      calc = obtener_porcentaje_similitud(acc1, acc2)

    return calc * point_weights['ACC']

  #COLOR
  def COL_punctuation(col1, col2):
    homologation={
      "blanco":['blanquito','palido','p?lido','alvino','albino','blankito','claro'],
      "amarillo":['rubio','dorado','gringo','rubiesito','doradito','gringuito'],
      "negro":['negrito','oscuro','oscuridad','noche', 'obscuro','oscurito'],
      "marron":['marroncito','marronsito','chocolate','tierra'],
      "gris":['plomo','plomito','grisesito']
    }

    for color in homologation:
      for value in homologation[color]:
        col1=col1.replace(value,color)
        col2=col2.replace(value,color)

    calc = obtener_porcentaje_similitud(col1, col2)
    return calc * point_weights['COL']

  #DAT
  def DAT_punctuation(dat1, dat2):
    dat2= dateTransformed
    dat1= transformDate(dat1)

    if dat2==-1 or dat1==-1:
      return 0

    daysBetween=(dat2-dat1).days
    calc=0
    if daysBetween < 40:
      calc= (40-daysBetween)/40*point_weights['DAT']
    return calc

  #DOG
  def DOG_punctuation(dog1,dog2):
    calc = obtener_porcentaje_similitud(dog1, dog2)
    return calc * point_weights['DOG']

  #HRS
  def HRS_punctuation(hrs1, hrs2):
    calc = obtener_porcentaje_similitud(hrs1, hrs2)
    return calc * point_weights['HRS']

  #PEL
  def PEL_punctuation(pel1,pel2):
    calc = obtener_porcentaje_similitud(pel1, pel2)
    return calc * point_weights['PEL']

  #PLC
  def PLC_punctuation(plc1,plc2):
    calc = obtener_porcentaje_similitud(plc1, plc2)
    return calc * point_weights['PLC']

  #RAZ
  def RAZ_punctuation(raz1, raz2):
    calc = obtener_porcentaje_similitud(raz1, raz2)
    return calc * point_weights['RAZ']

  #SEX
  def SEX_punctuation(sex1, sex2):
    calc = obtener_porcentaje_similitud(sex1, sex2)
    return calc * point_weights['SEX']

  #STT
  def STT_punctuation(stt1, stt2):
    calc = obtener_porcentaje_similitud(stt1, stt2)
    return calc * point_weights['STT']

  #TAM
  def TAM_punctuation(tam1, tam2):
    homologation={
        "peque?o":['chiquito','chico','peque?ito','pequeno','pequenito','enano','toy','chato'],
        "mediano":['medio','normal','promedio','medianito'],
        "grande":['grandote', 'enorme','gigante','grandesito','alto','gran']
    }

    for tamanio in homologation:
      for value in homologation[tamanio]:
        tam1=tam1.replace(value,tamanio)
        tam2=tam2.replace(value,tamanio)

    calc=0
    return calc * point_weights['TAM']

  NER_keys={
      'ACC':ACC_punctuation,
      'COL':COL_punctuation,
      'DAT':DAT_punctuation,
      'DOG':DOG_punctuation,
      'HRS':HRS_punctuation,
      'PEL':PEL_punctuation,
      'PLC':PLC_punctuation,
      'RAZ':RAZ_punctuation,
      'SEX':SEX_punctuation,
      'STT':STT_punctuation,
      'TAM':TAM_punctuation
  }

  if 'DAT' in NER_registro:
    dateTransformed=transformDate(NER_registro['DAT'])

  print('Puntos obtenidos en NER: ')
  for val in NER_compare:
    if val in NER_registro and val!='TLF':
      pointsGained=NER_keys[val](NER_compare[val], NER_registro[val])
      print(val,': ',pointsGained, '')
      points= points+ pointsGained


  return points

##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################


def calcPuntajeRaza (razas_registro, razas_compare):
  puntuaciones=[]
  punt=0
  multiplicador = 0
  for c, v in razas_compare.items():
    for clave, valor in razas_registro.items():
        if c==clave:
            peso=(v/100)*(valor/100)
            multiplicador+=peso
        else:
            mulitplicador=multiplicador
  puntuaciones.append({"puntuacion": round(multiplicador * 100)})

  print ("Puntos obtenidos raza: ", round(multiplicador*100))
  return round(multiplicador*100)


##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################

def calTotal(all_registros, main_registro):
  final_regs=[]
  for dog in all_registros:
    NER_points= CalcNERPoints(main_registro["NER"], dog["NER"])*point_weights['NER']
    IMG_points= calcPuntajeRaza(main_registro["imagen_razas"],dog["imagen_razas"])*point_weights['Image']
    saveImage(dog['imagen'], dog['name'])
    reg={
      'NER': dog['NER'],
      'NER_points':NER_points, 
      'Razas': dog['imagen_razas'],
      'IMG_points':IMG_points,
      'Total':NER_points+IMG_points, 
      'name':dog['name'], 
      'descripcion': dog['descripcion']
    }
    final_regs.append(reg)

  return final_regs

def saveImage(image_data, name):
  upload= "static\images\\"

  with open(upload+name, 'wb') as file:
    file.write(image_data)
