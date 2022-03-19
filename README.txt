This is a quick document detailing how to use the nestedsampler script for analysing isotropy of BBH mergers. If you have difficulties with 
specific issues, or believe a file is missing, feel free to email me at cs_islay667@protonmail.com.

1. First, you need data. You can grab the GWTC-1, GWTC-2, and GWTC-3 data from:

https://dcc.ligo.org/LIGO-P1800370/public
https://dcc.ligo.org/LIGO-P2000223/public
https://zenodo.org/record/5546663

These are large downloads, so only GWTC-1 is included in the Git repo.

2. Use the o3Unwrap.py and script to generate PSDs and smaller posterior files for events. You will need to add all the
events you want to process into the eventsList in each script; their last use case was for just O3b. The data at time of writing uses the waveform
templates IMRPhenomPv2 (GWTC-1), IMRPhenomPv3HM (GWTC-2), or IMRPhenomXPHM (GWTC-3), so o3Unwrap.py, common_func.py and detections.py are hardcoded to try
these 3 column names in the h5 files before falling back on the generic title 'posterior'. Future data might use a different waveform, so you may need to 
edit the o3Unwrap.py script to reflect this (or just use the header 'posterior', since all scripts should recognise this!)

3. Make sure the files are structured correctly. In general, you want:

parent directory > Data > Run_OX > Events (for generation of pickle files later)
parent directory > Data > Run_OX > Posterior_samples (for PSDs, apologies for naming convention)
parent directory > Data > GWTC-X (for Posterior samples you've downloaded and processed)
parent directory > Data > times (all the times.txt files for each event)
parent directory > Data > PSD_data (for detector PSDs, included in Repo with a source)

GWTC-1 is included in the Repo as an example of the structure. 

4. Make sure all paths in setup.py, common_func.py are set appropriately.

5. In setup.py for both pofd and pixel_version directories, set up the eventsList to include all events you want to analyse. Remove any NS events.

5. Run pofd.py script, making sure data=True and plots=True on line 366. If a KeyError due to pickle arises, make sure to update packages, 
and redownload the data.

6. Run pofd_marg.py script, setting data and plots to True on line 230.

7. in pixel_version, make sure all paths are set as desired.

8. Run nested_sampler.py and iso.py to get the evidence for the two models. You may want to downsample the nested_sampler.py script or increase the
number of threads.

9. In the output of both files, make a note of the log_evidence or log_Z. The subtraction of these two numbers is your log Bayes factor.


