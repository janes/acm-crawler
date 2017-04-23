import os
import gc

from databaseHelper import DatabaseHelper


offset= 10
breakIntervalInSeconds = 5

dbHelper = DatabaseHelper()


if dbHelper.connectToLocalDatabase() :

	print "\n\nstarting..."

	publications = dbHelper.getQueue(offset)	
	for publication in publications:						
		if not dbHelper.findPublication(str(publication[0])):
			print "waiting "+str(breakIntervalInSeconds)+" seconds to collect..."
			os.system("sleep "+str(breakIntervalInSeconds))	
			print "collecting "+str(publication[0])
			os.system("python parser.py "+str(publication[0]))
		else:
			dbHelper.removeFromQueue(str(publication[0]))	


	if not publications:
		print "Empty queue. Adding publications to collect..."
		for arg in ['1454023','1557029','1571977','1571978','1639720','1651290','1718510','1722966','1943453','1963412','1963481','2168569','2187895','2208343','2208695','2348313','2389387','2481248','2502057','2507205','2645728','2645751','2645770','2653361','2654946','2662070','2682719','2685287','2741997','2742826','2749344','2749399','2767746','2783268','2800175','2806222','2806503','2806511','2813511','2883038','2883069','2907089','2959132','2959134','2959143','2959149','2959150','2959155','2959159','2959165','2959170','2959172','2959178','2959182','2959190','2971729','3007290','3025177','3052581','3054182','3054183','3054185','544231','963775']:
			dbHelper.addToQueue(str(arg))	
		

	dbHelper.closeLocalConnection()
	gc.collect()
	os.system("python crawler.py")
	
else:
	print "not able to connect to local database. Check 'databaseHelper.py'"	