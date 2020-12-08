import _albedo.dataset as dataset
import param
import panel as pn
import datetime

class Parameters(dataset.DataSet):
    
    time = param.Selector(default=0, objects=[0,1])
    
    elev     = param.Integer(default=30, bounds=(0, 90), step=5)
    azim     = param.Integer(default=285, bounds=(0, 360), step=15)

    choose3d = param.ListSelector(default=['Pointcloud', 'Planar Fit'],
                                  objects=['Pointcloud', 'Planar Fit'])
    
    resolution = param.Integer(default=30, bounds=(10, 300), step=10)
    sigma      = param.Number(0.5, bounds=(0, 3))
    vertEx     = param.Number(1.0)
    
    set_measurements   = param.ListSelector(
                            default=['Global Up', 'Direct Dwn', 'Diffuse Dwn'],
                            objects=['Global Up', 'Direct Dwn', 'Diffuse Dwn'])
    set_planar_curves  = param.ListSelector(
                            default=['M','Alpha'], objects=['M','Alpha','IDR'])
    set_raster_curves  = param.ListSelector(
                            default=[], objects=['M','Alpha','IDR'])
    set_horizon_curves = param.ListSelector(
                            default=[], objects=['M','Alpha','IDR'])
    set_curve_filler   = param.ListSelector(
                            default=[], 
                            objects=['> Selected M\'s', '> Selected Alpha\'s', 
                                     '> Selected IDR\'s'])
    set_visibile_curve = param.Boolean(False)
    
    activateMask = param.Selector(default='Remove', objects=['Overlay', 'Remove'])
    bins = param.Integer(default=16, bounds=(8, 64), step=8)
    
    run = param.Boolean(False)
    
    log = param.String('')
    
    progress = pn.widgets.Progress(name='Progress', width=450, height=25,
                                   value=0, bar_color='info')
    
    modelComplete = param.ObjectSelector(default="Incomplete", 
                                         objects=["Incomplete", "Complete"])
    
    dictionary = param.Dict(default={"default": "dictionary"})