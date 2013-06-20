import numpy as np

vtk_template = """\
# vtk DataFile Version 2.0
VTK file autogenerated for nemo3d via nemo_evec_to_vtk script
ASCII
DATASET STRUCTURED_POINTS
DIMENSIONS %(nx)d %(ny)d %(nz)d
ORIGIN %(ox)f %(oy)f %(oz)f
SPACING %(sx)f %(sy)f %(sz)f
POINT_DATA %(npts)d
%(recordstrings)s
"""

record_template = """\
SCALARS %(name)s float 1
LOOKUP_TABLE default
%(datastring)s
"""

def iterator_3d(nxyz,oxyz,sxyz):
    nx,ny,nz = nxyz
    sx,sy,sz = sxyz
    ox,oy,oz = oxyz
    for i in xrange(nx):
        x = ox + i*sx
        for j in xrange(ny):
            y = oy + j*sy
            for k in xrange(nz):
                z = oz + k*sz
                yield x,y,z
    return

def image_orbitals(atoms,orbs,bfs,npts=20):
    xmin,xmax,ymin,ymax,zmin,zmax = atoms.bbox()
    oxyz = xmin,ymin,zmin
    sxyz = (xmax-xmin)/(npts-1.),(ymax-ymin)/(npts-1.),(zmax-zmin)/(npts-1.)
    nxyz = npts,npts,npts
    for orb in orbs:
        for c in orb:
            for bf in bfs:
                for x,y,z in iterator_3d(nxyz,oxyz,sxyz):
                    
    

def make_recordstrings(records,names):
    lines = []
    for name,record in zip(names,records):
        datastring = "\n".join("%f" % fi for fi in record)
        lines.append(record_template % dict(name=name,datastring=datastring))
    return "\n".join(lines)
        
def write_vtk(records,names,nxyz,oxyz,sxyz,fname = "nemo.vtk"):
    sx = sy = sz = sxyz
    ox = oy = oz = oxyz
    nx,ny,nz = nxyz
    npts = nx*ny*nz
    assert len(records) == len(names)
    assert npts == len(records[0])
    recordstrings = make_recordstrings(records,names)
    open(fname,"w").write(vtk_template % locals())
    return    
    
