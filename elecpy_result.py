import os,sys,glob,json
import numpy as np

class ElecpyResult(object):

    def __init__(self, path):
        self.path = path
        
        assert os.path.exists(path)

        self.files_vmem = sorted(glob.glob(os.path.join(path, 'vmem_*.npy')))
        self.files_phie = sorted(glob.glob(os.path.join(path, 'phie_*.npy')))
        self.dirs_cell  = sorted(glob.glob(os.path.join(path, 'cell_*')))

        assert len(self.files_vmem) == len(self.files_phie) == len(self.dirs_cell)
        
        self.shape = np.load(self.files_vmem[0]).shape
        
    def extract(self, list_val, mesh_pos = None, range_t = None):
        
        ret = {}
        for val in list_val:
            
            if range_t is None: range_t = np.arange(len(self.files_vmem))
            if mesh_pos is None: mesh_pos = np.meshgrid(*tuple([np.arange(s) for s in self.shape]))
            
            files = []
            for t in range_t:
                if val is 'vmem':
                    files.append(self.files_vmem[t])
                elif val is 'phie':
                    files.append(self.files_phie[t])
                else:
                    files.append( os.path.join(self.dirs_cell[t], '{0}.npy'.format(val)))        
            assert len(files)>0
            
            if val in ['vmem', 'phie']:
                ret[val] = np.array([ np.load(f)[mesh_pos].T for f in files ])
            else:
                ret[val] = np.array([ np.load(f).reshape(self.shape)[mesh_pos].T for f in files ])
            
        return (ret)