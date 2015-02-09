#!/home/dcolombo/anaconda/bin/python

"""
Create dendrograms and catalogs for
all datasets I have.
"""


import warnings
import os.path
import sys

import numpy as np
import math

from astrodendro import Dendrogram, ppv_catalog
from astropy import units as u
from astropy.io import fits
from astropy import wcs
from astropy.table.table import Column
from astropy.table import Table
#from scipy.ndimage.measurements import label

from datetime import datetime

from pdb import set_trace as stop


"""
#COMPLETE/opha_13co
vosdir = 'COMPLETE'
filename = 'opha_13co'
dist = 131
rms = 0.374575
pix_beam = 4.14680951294


#W51/w51_
vosdir = '/Volumes/Zeruel_data/W51/'
dist = 5.41*10**3

filename = vosdir+'w51_12co32'
rms = 0.516499
pix_beam = 5


filename = vosdir+'w51_13co32'
rms = 0.378883
pix_beam = 5


filename = vosdir+'w51_c18o32'
rms = 0.456995
pix_beam = 5


#PAWS
vosdir = '/Volumes/Zeruel_data/PAWS/'
filename = vosdir+'paws_hd'
rms = 0.4
pix_beam = 14
"""

vosdirs = ['ORION/','COMPLETE/','COMPLETE/','W51/','W51/','W51/','PAWS/','MILKY_WAY/','MILKY_WAY/','MILKY_WAY/']

"""
vosdirs = ['/Volumes/Zeruel_data/ORION/',\
           '/Volumes/Zeruel_data/COMPLETE/',\
           '/Volumes/Zeruel_data/COMPLETE/',\
           '/Volumes/Zeruel_data/W51/',\
           '/Volumes/Zeruel_data/W51/',\
           '/Volumes/Zeruel_data/W51/',\
           '/Volumes/Zeruel_data/PAWS/',\
           '/Volumes/Zeruel_data/MILKY_WAY/',\
           '/Volumes/Zeruel_data/MILKY_WAY/']
"""

           
filenames = ['orion', 'pera_13co','opha_13co','w51_12co32','w51_13co32','w51_c18o32','paws_hd','gc_cs','ogs','cygx']
pix_beams = [3*1.3, 3*4, 3*4, 3*5, 3*5, 3*5, 14, 3*2.5, 3*1, 3*4]
ch1is = [22, 0, 0, 0, 0, 0, 0, 0, 1, np.nan]
ch1fs = [24, 100, 100, 9, 9, 9, 30, 1, 80, np.nan] 
ch2is = [75, 400, 400, 275, 275, 275, 90, 86, 205, 310]
ch2fs = [79, -1, -1, -1, -1, -1, -1, -1, 235, 350]


# Control flow
do_prep = False
do_dendro = True
do_catalog = True
do_affmats = True

#outfile = 'all_data_dendro_parameters.npz'
#main_path = '/Volumes/Zeruel_data/W51/'
#main_path = './'

# Increase the recursion limit
sys.setrecursionlimit(100000)

selfiles = [9]

for j in selfiles:

    vosdir = vosdirs[j]
    filename = filenames[j]
    filemask = filenames[j]+'_dilmasked'
    pix_beam = pix_beams[j]
    ch1i = ch1is[j]
    ch1f = ch1fs[j]
    ch2i = ch2is[j]
    ch2f = ch2fs[j]        
    
    if do_prep:

        print "Starting masking for", filename

        hdu = fits.open(filename+'.fits', ignore_missing_end = True)[0]
        data = hdu.data
        hd = hdu.header

        if np.size(np.shape(data))==4:
            data = data[0,:,:,:]

        # Getting a very rought estimation of rms   
        free1 = data[ch1i:ch1f,:,:]
        free2 = data[ch2i:ch2f,:,:]
        freeT = np.concatenate((free1,free2), axis=0) 

        rmsmap = np.std(freeT, axis=0)
        s2ncube = np.zeros(data.shape)

        for v in range(data.shape[0]):
            s2ncube[v,:,:] = data[v,:,:]/rmsmap[:,:]

        rms = np.median(rmsmap[np.isfinite(rmsmap)])

        # This is CPROPS'dilate mask (too slow...)
        """
        mask_in = np.zeros(data.shape)
        mask_in[s2ncube > 2] = 1

        constraint = np.zeros(data.shape)        
        constraint[s2ncube > 4] = 1

        mask = (mask_in*constraint)+constraint
        labregs, numregs = label(mask > 0)

        mask_out = np.zeros(data.shape)
        
        for l in range(1,numregs+1):
            if np.sum(mask[labregs == l] == 2) > 1:
                mask_out[labregs == l] = 1
            
        """
        data[s2ncube < 2] = np.nan
            
        
        data = fits.PrimaryHDU(data.astype('float'), hdu.header)
        os.system("rm -rf "+filename+'_masked.fits')
        print 'Write '+filename+'_masked.fits'        
        data.writeto(filename+'_masked.fits')

        os.system('vcp --overwrite '+filename+'_masked.fits vos:dcolombo/cloudstering2/'+vosdir)

        """
        s2ncube = fits.PrimaryHDU(s2ncube.astype('float'), hdu.header)
        os.system("rm -rf "+filename+'_s2ncube.fits')
        print 'Write '+filename+'_s2ncube.fits'        
        s2ncube.writeto(filename+'_s2ncube.fits')

        os.system('vcp --overwrite '+filename+'_s2ncube.fits vos:dcolombo/cloudstering2/'+vosdir)                     
        """
                    
                
    if do_dendro:

        print "Generating dendrogram of", filemask
        
        mhdu = fits.open(filemask+'.fits', ignore_missing_end = True)[0]
        mdata = mhdu.data
        mhd = mhdu.header

        if np.size(np.shape(mdata))==4:
            mdata = mdata[0,:,:,:]

            
        dhdu = fits.open(filename+'.fits', ignore_missing_end = True)[0]
        ddata = dhdu.data
        dhd = dhdu.header

        if np.size(np.shape(ddata))==4:
            ddata = ddata[0,:,:,:]            

            
        # Getting a very rought estimation of rms   
        #free1 = ddata[ch1i:ch1f,:,:]
        #free2 = ddata[ch2i:ch2f,:,:]
        #freeT = np.concatenate((free1,free2), axis=0)
        freeT = ddata[ch2i:ch2f,:,:]    

        rmsmap = np.std(freeT, axis=0)
        rms = np.median(rmsmap[np.isfinite(rmsmap)])        

        d = Dendrogram.compute(mdata, min_value=0, min_delta=2*rms, min_npix=pix_beam, verbose = 0)    
        d.save_to(filemask+'_dendrogram.fits')

        os.system('vcp --overwrite '+filemask+'_dendrogram.fits vos:dcolombo/cloudstering2/'+vosdir)


        
    if do_catalog:
                        
        print 'Load dendrogram file: ', filemask
        d = Dendrogram.load_from(filemask+'_dendrogram.fits')    

        # Making the catalog
        print "Making a simple catalog of dendrogram structures"
        metadata = {}
        metadata['data_unit'] = u.Jy #This should be Kelvin!

        cat = ppv_catalog(d, metadata)
        volumes = np.pi*cat['radius'].data**2*cat['v_rms'].data

        cat.add_column(Column(name='luminosity', data=cat['flux'].data))
        cat.add_column(Column(name='volume', data=volumes))        
        
        # Save the catalog
        os.system('rm -rf '+filemask+'_catalog.fits')
        cat.write(filemask+'_catalog.fits')
        os.system('vcp --overwrite '+filemask+'_catalog.fits vos:dcolombo/cloudstering2/'+vosdir)


        
    if do_affmats:
        
        dendrogram = Dendrogram.load_from(filemask+'_dendrogram.fits')
        catalog = Table.read(filemask+'_catalog.fits')
    
        all_structures_idx = range(len(catalog['radius'].data))

        all_leav_names = []
        all_leav_idx = []

        all_brc_names = []
        all_brc_idx = []

        all_parents = []
        all_children = []

        trunk_brs_idx = []
        two_clust_idx = []    
        mul_leav_idx = []
    
        for structure_idx in all_structures_idx:

            s = dendrogram[structure_idx]

            # If structure is a leaf find all the parents
            if s.is_leaf and s.parent != None:

                par = s.parent
                all_leav_names.append(str(s.idx))

                parents = []
            
                while par != None:

                    parents.append(par.idx)
                    par = par.parent
                
                parents.append(len(catalog['radius'].data)) # This is the trunk!
                all_parents.append(parents)
            
            
            # If structure is a brach find all its leaves
            if s.is_branch:

                all_brc_idx.append(s.idx)
                all_brc_names.append(str(s.idx))
            
                children = []
            
                for leaf in s.sorted_leaves():

                    children.append(leaf.idx)
                
                all_children.append(children)

                # Trunk branches
                if s.parent == None:

                    trunk_brs_idx.append(s.idx)
                    all_leav_idx = all_leav_idx + children

                    if s.children[0].is_branch or s.children[1].is_branch:
                        mul_leav_idx = mul_leav_idx + children
                    else:
                        two_clust_idx.append(s.idx)
        
        two_clust_idx = np.unique(two_clust_idx).tolist()
    
        dict_parents = dict(zip(all_leav_names,all_parents))            
        dict_children = dict(zip(all_brc_names,all_children))    
    
        # Retriving needed properties from the catalog
        volumes = catalog['volume'].data
        luminosities = catalog['luminosity'].data

        t_volume = sum(volumes[trunk_brs_idx])
        t_luminosity = sum(luminosities[trunk_brs_idx])

        volumes = volumes.tolist()
        luminosities = luminosities.tolist()

        volumes.append(t_volume)
        luminosities.append(t_luminosity)       
    
        dict_props = {'volumes':volumes, 'luminosities':luminosities}


        print "Making affinity matrices"
    
        num = len(all_leav_idx)        
        WAs = np.zeros((2,num,num))

        volumes = dict_props['volumes']
        luminosities = dict_props['luminosities']

        # Collecting affinities only for branch mergers
        
        # Let's save one for loop
        n2 = num**2
        yy = np.outer(np.ones(num, dtype = np.int),range(num))
        xx = np.outer(range(num),np.ones(num, dtype = np.int))
        yy = yy.reshape(n2)
        xx = xx.reshape(n2)                

        tr_idx = len(volumes)-1
        
        # Going through the branch
        for lp in range(len(xx)):

            icont = xx[lp]
            jcont = yy[lp]
            
            i_idx = all_leav_idx[icont]
            imat = all_leav_idx.index(i_idx)
        
            if icont > jcont:
                
                j_idx = all_leav_idx[jcont]
                jmat = all_leav_idx.index(j_idx)
            
                ipars = dict_parents[str(i_idx)]
                jpars = dict_parents[str(j_idx)]

                # Find shorter list for the comparison
                lpars = min(ipars,jpars)

                # Finding the common parents
                aux_commons = list(set(ipars).intersection(set(jpars)))

                commons = [x for x in lpars if x in aux_commons]
                pi_idx = commons[0]

                if pi_idx != tr_idx:
            
                    ch1_idx = dendrogram[pi_idx].children[0].idx
                    ch2_idx = dendrogram[pi_idx].children[1].idx
                
                
                else:

                    ch1_idx = dendrogram[i_idx].ancestor.idx
                    ch2_idx = dendrogram[j_idx].ancestor.idx
                                            
                            
                # Volume
                wij = volumes[pi_idx]
                WAs[0,imat,jmat] = wij
                WAs[0,jmat,imat] = wij
            
                # Luminosity
                wij = luminosities[pi_idx]
                WAs[1,imat,jmat] = wij
                WAs[1,jmat,imat] = wij


        # Save the affinities
        os.system('rm -rf '+filemask+'_affmats.npy')
        np.save(filemask+"_affmats.npy", WAs)
        os.system('vcp --overwrite '+filemask+'_affmats.npy vos:dcolombo/cloudstering2/'+vosdir)
            
    #stop()
        
# Default recursion limit
sys.setrecursionlimit(1000)
