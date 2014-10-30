#!/usr/bin/python
# -*- coding: utf-8 -*-
#import xml.etree.ElementTree as ET, urllib, gzip, io
import datetime
import urllib, gzip, io
import MySQLdb as db
import getpass
from lxml import etree as ET


username = raw_input("Enter your username: ")
password=getpass.getpass("Enter your password: ")
conn = db.connect("localhost", username, password, "resonances", \
                         use_unicode=True, charset="utf8")
c = conn.cursor(db.cursors.DictCursor)
litc = conn.cursor(db.cursors.DictCursor)
starAliasc = conn.cursor(db.cursors.DictCursor)
planetAliasc = conn.cursor(db.cursors.DictCursor)
c.execute("select Star.Name as SName, \
                 Star.Mass as SMass, Star.MassError as SMassError, \
                 Star.MassErrorMinus as SMassErrorMinus, \
                 Star.Metallicity as SMetallicity, \
                 Star.MetallicityError as SMetallicityError, \
                 Star.MetallicityErrorMinus as SMetallicityErrorMinus, \
                 Star.Age as SAge, Star.AgeError as SAgeError, \
                 Star.AgeErrorMinus as SAgeErrorMinus, \
                 Star.Temperature as STemperature, \
                 Star.TemperatureError as STemperatureError, \
                 Star.TemperatureErrorMinus as STemperatureErrorMinus, \
                 Star.Distance as SDistance, \
                 Star.DistanceError as SDistanceError, \
                 Star.DistanceErrorMinus as SDistanceErrorMinus, \
                 Planets.StarName, Planets.Name, Planets.coordSystem, \
                 mSinI, massOperator, \
                 Planets.Mass, Planets.MassError, Planets.MassErrorMinus, \
		 Planets.massComputed, \
                 massJupitersOperator, \
                 massJupiters, massJupitersError, massJupitersErrorMinus, \
		 Planets.massJupitersComputed, \
                 Planets.Radius, Planets.radiusError, Planets.radiusErrorMinus, \
                 Planets.radiusComputed, Planets.radiusPrec, \
		 Planets.massJupitersComputed, \
                 Planets.RadiusJupiters, Planets.radiusJupitersError, \
                 Planets.radiusJupitersErrorMinus, \
                 Planets.radiusJupitersComputed, Planets.radiusJupitersPrec, \
                 Axis, AxisError, AxisErrorMinus, \
                 Period, periodError, periodErrorMinus, \
                 TperiUnits, \
                 Tperi, TperiError, TperiErrorMinus, \
                 BigOmega, BigOmegaError, BigOmegaErrorMinus, \
                 Omega, OmegaError, OmegaErrorMinus, \
                 meanLongitude, meanLongitudeError, meanLongitudeErrorMinus, \
                 meanAnomaly, meanAnomalyError, meanAnomalyErrorMinus, \
                 argumentOfLatitude, argumentOfLatitudeError, argumentOfLatitudeErrorMinus, \
                 meanArgOfLatitude, meanArgOfLatitudeError, meanArgOfLatitudeErrorMinus, \
                 p,q, \
                 Planets.eOperator, \
                 Eccentricity, EccentricityError, EccentricityErrorMinus, \
                 Planets.Inclination, Planets.InclinationError, \
                 Planets.InclinationErrorMinus, \
                 Planets.tTransitUnit, \
                 Planets.tTransit, Planets.tTransitError, \
                 Planets.tTransitErrorMinus, \
                 Planet1, Planet2, Status, \
                 omegaTilde, omegaTildeError, omegaTildeErrorMinus, \
                 epochUnit, Epoch, EpochError, EpochErrorMinus, \
                 Resonances.Id as ResId, Id, LastUpdated \
            from Star, resonances.Planets \
            left join (resonances.Resonances) on \
                 Resonances.StarName=Planets.StarName and \
                 (Planets.Name=Resonances.Planet1) \
            where \
                 Star.Name = Planets.StarName \
            group by \
                 Planets.Name, Planets.StarName \
            order by \
                 Planets.StarName, Planets.Period")

systemname = ""
for record in c.fetchall():
   if record['StarName'] != systemname:
      system = ET.Element('system')
      starAliasc.execute("select * from StarAlias where \
                                 StarAlias.StarName = \""+record['StarName']+"\"")
      for starAliasRecord in starAliasc.fetchall():
         systemName=ET.SubElement(system,'name')
         if starAliasRecord['toExport'] == 1:
            filename = starAliasRecord['Alias']
	 systemName.text = starAliasRecord['Alias']


      distance = ET.SubElement(system, 'distance')
      star = ET.SubElement(system, 'star')
      starMass = ET.SubElement(star,'mass')
      metallicity = ET.SubElement(star, 'metallicity')
      age = ET.SubElement(star, 'age')
      temperature = ET.SubElement(star, 'temperature')
      starMass.text = str(record['SMass'])
      metallicity.text = str(record['SMetallicity'])
      if record['SMetallicityErrorMinus']:
         metallicity.set('errorminus', str(-record['SMetallicityErrorMinus']))
      if record['SMetallicityError']:
         metallicity.set('errorplus', str(record['SMetallicityError']))
      age.text = str(record['SAge'])
      if record['SAgeErrorMinus']:
         age.set('errorminus', str(-record['SAgeErrorMinus']))
      if record['SAgeError']:
         age.set('errorplus', str(record['SAgeError']))
      
      temperature.text = str(record['STemperature'])
      distance.text = str(record['SDistance'])

      systemname = record['StarName']
      i = 0
      resonance=[]

   planet = ET.SubElement(star, 'planet')

   planetAliasc.execute("select StarAlias.Alias as sAlias, \
                         PlanetAlias.Alias as pAlias from StarAlias \
			 join (PlanetAlias) on PlanetAlias.StarAliasId=StarAlias.Id \
			 where PlanetAlias.PlanetName = \"" + record['Name'] + "\" \
			 and StarAlias.StarName = \"" + record['StarName'] + "\";")
   for planetNameRow in planetAliasc.fetchall():
      planetName = ET.SubElement(planet, 'name')
      planetName.text = planetNameRow['sAlias'] + ' ' + planetNameRow['pAlias']

   coordSystem = ET.SubElement(planet, 'coordinates')
   if (record['mSinI'] == 's'):
      mass = ET.SubElement(planet, 'massearthssini')
   else:
      mass = ET.SubElement(planet, 'massearths')
   if (record['mSinI'] == 's'):
      massjup = ET.SubElement(planet, 'massjupiterssini')
   else:
      massjup = ET.SubElement(planet, 'massjupiters')
   planetradius = ET.SubElement(planet, 'radius')
   planetradiusjupiters = ET.SubElement(planet, 'radiusjupiters')
   period = ET.SubElement(planet, 'period')
   axis = ET.SubElement(planet, 'semimajoraxis')
   eccentricity = ET.SubElement(planet, 'eccentricity')
   inclination = ET.SubElement(planet, 'inclination')
   timeOfPericentre = ET.SubElement(planet, 'timeofpericentre')
   ascendingNode = ET.SubElement(planet, 'ascendingnode')
   periastron = ET.SubElement(planet, 'periastron')
   argumentOfPeriastron = ET.SubElement(planet,'argumentofperiastron')
   longitude = ET.SubElement(planet, 'longitude')
   meananomaly = ET.SubElement(planet, 'meananomaly')
   argoflatitude = ET.SubElement(planet, 'argoflatitude')
   meanargoflatitude = ET.SubElement(planet, 'meanargoflatitude')
   transittime = ET.SubElement(planet,'transittime')
   epoch = ET.SubElement(planet,'epoch')
   status = ET.SubElement(planet, 'status')
   lastUpdate = ET.SubElement(planet, 'lastupdate')

   coordSystem.text = record['coordSystem']
   if record['massOperator'] == '&lt;':
      if record['Mass']:
         mass.set('upperlimit', str(record['Mass']))
      elif record['massComputed']:
         mass.set('upperlimit', str(record['massComputed']))
         mass.set('computed','true')

      if record['massJupiters']:
         massjup.set('upperlimit', str(record['massJupiters']))
      elif record['massJupitersComputed']:
         massjup.set('upperlimit',str (record['massJupitersComputed']))
         massjup.set('computed','true')
   else:
      if record['Mass']:
         mass.text = str(record['Mass'])
         if record['MassErrorMinus']:
            mass.set('errorminus', str(-record['MassErrorMinus']))
         if record['MassError']:
            mass.set('errorplus', str(record['MassError']))
      elif record['massComputed']:
         mass.text = str(record['massComputed'])
         mass.set('computed','true')

      if record['massJupiters']:
         massjup.text = str(record['massJupiters'])
         if record['massJupitersErrorMinus']:
            massjup.set('errorminus', str(-record['massJupitersErrorMinus']))
         if record['massJupitersError']:
            massjup.set('errorplus', str(record['massJupitersError']))
      elif record['massJupitersComputed']:
         massjup.text = str (record['massJupitersComputed'])
         massjup.set('computed','true')

      if record['Radius']:
         planetradius.text = str(record['Radius'])
         if record['radiusError']:
            planetradius.set('errorminus', str(-record['radiusErrorMinus']))
         if record['radiusError']:
            planetradius.set('errorplus', str(record['radiusError']))
      elif record['radiusComputed']:
         planetradius.text = str (record['radiusComputed'])
         planetradius.set('computed','true')
         if record['radiusError']:
            planetradius.set('errorminus', str(-record['radiusErrorMinus']))
         if record['radiusError']:
            planetradius.set('errorplus', str(record['radiusError']))

      if record['RadiusJupiters']:
         planetradiusjupiters.text = str(record['RadiusJupiters'])
         if record['radiusJupitersErrorMinus']:
            planetradiusjupiters.set('errorminus', str(-record['radiusJupitersErrorMinus']))
         if record['radiusJupitersError']:
            planetradiusjupiters.set('errorplus', str(record['radiusJupitersError']))
      elif record['radiusJupitersComputed']:
         planetradiusjupiters.text = str (record['radiusJupitersComputed'])
         planetradiusjupiters.set('computed','true')
         if record['radiusJupitersErrorMinus']:
            planetradiusjupiters.set('errorminus', str(-record['radiusJupitersErrorMinus']))
         if record['radiusJupitersError']:
            planetradiusjupiters.set('errorplus', str(record['radiusJupitersError']))

   period.text = str(record['Period'])
   if record['periodErrorMinus']:
      period.set('errorminus', str(-record['periodErrorMinus']))
   if record['periodError']:
      period.set('errorplus', str(record['periodError']))
   axis.text = str(record['Axis'])
   if record['AxisErrorMinus']:
      axis.set('errorminus', str(-record['AxisErrorMinus']))
   if record['AxisError']:
      axis.set('errorplus', str(record['AxisError']))
   if record['eOperator'] == '&lt;':
      eccentricity.set('upperlimit', str(record['Eccentricity']))
   else:
      eccentricity.text = str(record['Eccentricity'])
      if record['EccentricityErrorMinus']:
         eccentricity.set('errorminus',str(-record['EccentricityErrorMinus']))
      if record['EccentricityError']:
         eccentricity.set('errorplus',str(record['EccentricityError']))

   inclination.text = str(record['Inclination'])
   if record['InclinationErrorMinus']:
      inclination.set('errorminus',str(-record['InclinationErrorMinus']))
   if record['InclinationError']:
      inclination.set('errorplus',str(record['InclinationError']))
   timeOfPericentre.text = str(record['Tperi'])
   if record['TperiErrorMinus']:
      timeOfPericentre.set('errorminus', str(-record['TperiErrorMinus']))
   if record['TperiError']:
      timeOfPericentre.set('errorplus', str(record['TperiError']))
   ascendingNode.text = str(record['BigOmega'])
   if record['BigOmegaErrorMinus']:
      ascendingNode.set('errorminus', str(-record['BigOmegaErrorMinus']))
   if record['BigOmegaError']:
      ascendingNode.set('errorplus', str(record['BigOmegaError']))
   periastron.text = str(record['omegaTilde'])
   if record['omegaTildeErrorMinus']:
      periastron.set('errorminus', str(-record['omegaTildeErrorMinus']))
   if record['omegaTildeError']:
      periastron.set('errorplus', str(record['omegaTildeError']))
   argumentOfPeriastron.text = str(record['Omega'])  
   if record['OmegaErrorMinus']:
      argumentOfPeriastron.set('errorminus', str(-record['OmegaErrorMinus']))
   if record['OmegaError']:
      argumentOfPeriastron.set('errorplus', str(record['OmegaError']))

   meananomaly.text = str(record['meanAnomaly'])  
   if record['meanAnomalyErrorMinus']:
      meananomaly.set('errorminus', str(-record['meanAnomalyErrorMinus']))
   if record['meanAnomalyError']:
      meananomaly.set('errorplus', str(record['meanAnomalyError']))

   longitude.text = str(record['meanLongitude'])  
   if record['meanLongitudeErrorMinus']:
      longitude.set('errorminus', str(-record['meanLongitudeErrorMinus']))
   if record['meanLongitudeError']:
      longitude.set('errorplus', str(record['meanLongitudeError']))

   argoflatitude.text = str(record['argumentOfLatitude'])  
   if record['argumentOfLatitudeErrorMinus']:
      argoflatitude.set('errorminus', str(-record['argumentOfLatitudeErrorMinus']))
   if record['argumentOfLatitudeError']:
      argoflatitude.set('errorplus', str(record['argumentOfLatitudeError']))

   meanargoflatitude.text = str(record['meanArgOfLatitude'])  
   if record['meanArgOfLatitudeErrorMinus']:
      meanargoflatitude.set('errorminus', str(-record['meanArgOfLatitudeErrorMinus']))
   if record['meanArgOfLatitudeError']:
      meanargoflatitude.set('errorplus', str(record['meanArgOfLatitudeError']))

   transittime.text = str(record['tTransit'])  
   if record['tTransitUnit']:
      transittime.set('unit', record['tTransitUnit'])
   if record['tTransitErrorMinus']:
      transittime.set('errorminus', str(-record['tTransitErrorMinus']))
   if record['tTransitError']:
      transittime.set('errorplus', str(record['tTransitError']))

   epoch.text = str(record['Epoch'])  
   if record['epochUnit']:
      epoch.set('unit', record['epochUnit'])

   status.text = record['Status']
   lastUpdate.text=str(record['LastUpdated']).replace('-', '/')
   
 
   if record['p'] and record['q']:
      resonance.append( ET.SubElement(system, 'resonance'))
      p = ET.SubElement(resonance[i], 'p')
      q = ET.SubElement(resonance[i], 'q')
      p.set('p', str(record['p']))
      q.set('q', str(record['q']))
      p.text = str(record['Planet1'])
      q.text = str(record['Planet2'])
      litc.execute("select * from Literature where ResId = \
                                             "+str(record['ResId']))
      literature = []
      j = 0
      for litrow in litc.fetchall():
         literature.append(ET.SubElement(resonance[i],'literature'))
         title = ET.SubElement(literature[j], 'title')
         authors = ET.SubElement(literature[j], 'authors')
         link = ET.SubElement(literature[j], 'link')
         publisher = ET.SubElement(literature[j], 'publisher')
         j = j + 1
         title.text = litrow['Title']
         authors.text = litrow['Authors']
         authors.set('ordering', litrow['Ordering'])
         link.text = litrow['Link']
         publisher.text = litrow['Publisher']
      i = i + 1
   tree = ET.ElementTree(system)
   tree.write('resonances/'+filename+'.xml', pretty_print = True, encoding="utf-8")
