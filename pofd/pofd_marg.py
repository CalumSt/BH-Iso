import numpy as np
import healpy as hp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathos.multiprocessing import ProcessingPool
import time
import lal
import scipy.interpolate
import scipy.integrate

import setup as p
import common_func as cf


class PofdMarg:
    def __init__(self):
        self.__DL = np.linspace(1, p.dmax, p.dsize)
        self.__nPix = hp.nside2npix(p.nsideDet)
        self.__pixArr = range(self.__nPix)
        self.__pixArea = hp.nside2pixarea(p.nsideDet)
        self.loadEvents()
        self.loadRuns()

    def loadEvents(self):
        self.eventsList = []
        for item in p.eventsList:
            s = cf.loadSamples(item['postSamplePath'])
            dictData = {'run': item['run'],
                        'name': item['name'],
                        'right_ascension': s['right_ascension'],
                        'declination': s['declination'],
                        'time0': item['time'],
                        'pofdMarg': cf.openPickle(item['pofdMargPath']),
                        'pofd': cf.openPickle(item['pofdPath']),}
            self.eventsList.append(dictData)

    def loadRuns(self):
        self.runsList = []
        for item in p.runsList:
            dictData = {'run': item['run'],
                        'obsTime': np.genfromtxt(item['obsTpath'], names=True),
                        'pofd': cf.openPickle(item['pofdPath']),
                        'pofdMarg': cf.openPickle(item['pofdMargPath']),
                        'pofdMean': cf.openPickle(item['pofdAvPath']),}
            self.runsList.append(dictData)

    def __survivalFunc(self, dataPofd):
        """
        Returns the interpolated function of the probability of detection
        at a given distance at each pixel.
        """
        return scipy.interpolate.interp1d(self.__DL, dataPofd, bounds_error=False, fill_value=1e-10)


    def __pdfDet(self, d, RA, Dec, survFunc, gmstrad=0.0):
        """
        Returns the probability of detection when given luminosity distance (Mpc),
        right ascension, declination, and time (radians)
        """
        hpxmap = survFunc(d)[self.__pixArr]
        return hp.get_interp_val(hpxmap, np.pi/2.0 - Dec, RA - gmstrad)

    def __pdfDist(self, d):
        """Return the probability of the given distance (!!!Static universe model!!!)"""
        return 3.0/np.power(p.dmax, 3)*np.power(d, 2)

    def __margPdfDet(self, RA, Dec, survFunc):
        """Returns the marginalised (over distance) probability of detection at a given sky position."""
        I = lambda x: self.__pdfDet(x, RA, Dec, survFunc)*self.__pdfDist(x)
        return scipy.integrate.quad(I, 1, p.dmax)[0]

    def __calculGrid(self):
        """Calculate the marginalised probability of detection on a grid"""
        pool = ProcessingPool(p.pools)
        theta, phi = hp.pix2ang(p.nsideDet, self.__pixArr)
        raGrid, decGrid = phi, np.pi/2 - theta

        for item, itemPath in zip(self.runsList, p.runsList):
            survFunc = self.__survivalFunc(item['pofd'])
            print('Computing the grid for %s' % item['run'])
            def loopKiller(i):
                return self.__margPdfDet(raGrid[i], decGrid[i], survFunc)
            loopOut = pool.map(loopKiller, range(self.__nPix))
            result = np.hstack(loopOut)
            cf.savePickle(result, itemPath['pofdMargPath'])
            print('Calculated the grid!')
        self.loadRuns()
        pool.close()
        pool.join()
        pool.clear()

        pool = ProcessingPool(p.pools)
        theta, phi = hp.pix2ang(p.nsideDet, self.__pixArr)
        raGrid, decGrid = phi, np.pi/2 - theta
        for item, itemPath in zip(self.eventsList, p.eventsList):
            print('pofd shape, ', item['pofd'].shape)
            survFunc = self.__survivalFunc(item['pofd'])
            print('Computing the grid for %s' % item['name'])
            def loopKiller(i):
                return self.__margPdfDet(raGrid[i], decGrid[i], survFunc)
            loopOut = pool.map(loopKiller, range(self.__nPix))
            result = np.hstack(loopOut)
            print('result shape, ', result.shape)
            cf.savePickle(result, itemPath['pofdMargPath'])
            print('Calculated the grid!')
            self.loadRuns()
        pool.close()
        pool.join()
        pool.clear()

    def __pdfDetMargInterp(self, RA, Dec, mapDet, gmstrad):
        return hp.get_interp_val(mapDet, np.pi/2.0 - Dec, RA - gmstrad)

    def __gps2rad(self, gps):
        gpsLigo = lal.LIGOTimeGPS(gps)
        return lal.GreenwichMeanSiderealTime(gpsLigo)

    def __pdfDetRotation(self):
        """Calculaters the average the probability of detection over the run period"""
        self.loadRuns()
        pool = ProcessingPool(p.pools)
        for itemPath, itemRun in zip(p.runsList, self.runsList):
            obj = itemRun['pofdMarg']
            mapDet = obj[self.__pixArr]
            theta, phi = hp.pix2ang(p.nsideDet, self.__pixArr)
            RA, Dec = phi, np.pi/2.0 - theta

            data = itemRun['obsTime']
            gmstStart = data['GMSTstart']
            gmstEnd = data['GMSTend']
            obsTime = np.sum(gmstEnd - gmstStart)
            N = gmstStart.size

            print('Averaging pdf of detection over one day for %s' %(itemRun['run']))
            start = time.time()
            def loopKiller(i):
                res = np.zeros(self.__nPix)
                for j in range(self.__nPix):
                    I = lambda t: self.__pdfDetMargInterp(RA[j], Dec[j], mapDet, t)
                    res[j] = scipy.integrate.quad(I, gmstStart[i], gmstEnd[i])[0]
                return res

            loopOut = pool.map(loopKiller, range(N))
            loopOut = np.vstack(loopOut)
            result = np.sum(loopOut, axis=0)/obsTime
            cf.savePickle(result, itemPath['pofdAvPath'])
            print('Done with taking the average for %s!' %(itemRun['run']))
            print('Time taken: %.3f' %(time.time() - start))
        pool.close()
        pool.join()
        pool.clear()

    def plotMap(self, hpMap, path, events):
        plt.rcParams['font.serif']='Times New Roman' # Text font
        plt.rcParams['font.family']='serif'
        plt.rcParams['font.size']=12
        plt.rcParams['text.usetex']=False
        plt.rcParams['mathtext.fontset']='cm' #Computer Modern font
        figwidth=3.4 # PRD column width in inches
        aspect = 0.75 # Aspect ratio
        figheight = aspect*figwidth

        plt.figure(figsize=(figwidth,figheight),dpi=150)
        hp.mollview(hpMap, title='')

        for event in events:
            rai, thetai = event['right_ascension'],event['declination']
            phi, theta = rai, np.pi/2 - thetai
            if len(events) == 1:
                hp.projscatter(theta, phi, s=0.05, color='red',label=event['name'])
            else:
                hp.projscatter(theta, phi, s=0.05,label=event['name'])
        plt.legend()
        plt.savefig(path, dpi=150)
        plt.close('all')

    def run(self, data=True, plots=True):
        if data == True:
            self.__calculGrid()
            self.__pdfDetRotation()

        if plots == True:
            print('Plotting..')
            self.loadRuns()
            self.loadEvents()
            for run in self.runsList:
                print('Plotting '+run['run'])
                path = p.mapPath %(run['run'])
                obj = run['pofdMean']
                hpMap = obj[self.__pixArr]
                self.plotMap(hpMap=hpMap, path=path, events=[e for e in self.eventsList if e['run']==run['run']])
            for event in self.eventsList:
                print('Plotting '+event['name'])
                path = p.mapPath %(event['name'])
                obj = event['pofdMarg']
                hpMap = obj[self.__pixArr]
                self.plotMap(hpMap=hpMap, path=path, events=[event])

def main():
    prob = PofdMarg()
    prob.run(data=True, plots=True)

if __name__=='__main__':
    main()
