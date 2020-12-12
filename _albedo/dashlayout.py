import _albedo.dashcontrols as dashcontrols
import param
import panel as pn
import matplotlib.pyplot as plt
import markdown
import numpy as np
import os

class DashLayout(dashcontrols.DashControls):
    
    def return_README(self):
        with open('README.md','r') as f:
            html = markdown.markdown(f.read())
        return html
    
    @param.depends('run_state')
    def triptych_dispatch(self):
        if self.run_state == True:
            pass
        else:
            return self.triptych
    
    @param.depends('run_state')
    def dyptich_dispatch(self):
        if self.run_state == True:
            pass
        else:
            return self.diptych
    
    @param.depends('run_state')
    def polar_dispatch(self):
        if self.run_state == True:
            pass
        else:
            return self.polarAxes
        
    @param.depends('run_state')
    def timeseries_dispatch(self):
        if self.run_state == True:
            pass
        else:
            return self.timeSeries_Plot
            
    @param.depends('run_state')
    def video_dispatch(self):
        if self.run_state == True:
            pass
        else:
            vid_path = os.path.join(os.getcwd(), 'exports', 'animation.mp4')
            return pn.pane.Video(vid_path, loop=False)
    
    @param.depends('date')
    def return_time_control(self):
        return pn.Param(
                self.param, parameters=['time'],
                widgets={'time':{'widget_type': pn.widgets.DiscreteSlider, 
                                 'width': 180}},
                         width=200, name='Preview')
    
    @param.depends('dictionary')
    def return_config_dict(self):
        return pn.pane.JSON(self.dictionary, name='JSON', width=300, 
                            theme='dark', depth=2, hover_preview=True)
        
    
    @param.depends('log')
    def return_log_pane(self):
        return pn.pane.HTML(
        f"""
        <div style="overflow-y:scroll;position:relative;bottom:0;height:400px;">
        <pre style="color:white; font-size:12px">Build Log</pre>
        <pre style="color:deepskyblue; font-size:12px">{self.log}</pre>
        </div>
        """,
        style={'background-color':'#000000', 'border':'2px solid black',
               'border-radius': '5px', 'padding': '10px','width':'560px'}
    )
    
    @param.depends('modelComplete')
    def return_model_df(self):
        if self.modelComplete == 'Incomplete':
            return pn.Row('Run model to generate dataframe.')
        else:
            return pn.pane.DataFrame(self.model_dataframe, 
                                     max_rows=4, max_cols=7, width=900)
    
    @param.depends('dictionary')
    def reset_run_state(self):
        self.run = False
        self.progress.value = 0
        if self.modelComplete == 'Complete':
            self.modelComplete = 'Incomplete'
            del self.model_dataframe
        return
    
    @param.depends('modelComplete')
    def return_run_button(self):
        args = dict({'width': 80, 'name':'', 'parameters':['run']})
        enabled = pn.Param(
            self.param, **args, 
            widgets={'run':
                     {'widget_type': pn.widgets.Toggle, 'disabled':False},})
        disabled = pn.Param(
            self.param, **args, 
            widgets={'run':
                     {'widget_type': pn.widgets.Toggle, 'disabled':True},})
        if self.modelComplete == 'Incomplete':
            return enabled
        elif self.modelComplete == 'Complete':
            return disabled
        
    @param.depends('')
    
    def set_layout(self):
        self.function_row = pn.Row(
            self.set_filename, self.set_dataframe, self.set_raster,
            self.set_axes, self.set_m, self.set_masks, self.run_model, 
            self.reset_run_state, self.update_config
        )
        self.config_accordion = pn.Tabs(
            pn.Row(self.triptych_dispatch,
                   name='Raster Preview',
                   width=900
                  ),
            pn.Column(pn.Row(self.polar_dispatch, self.dyptich_dispatch),
                      name='Azimuth Preview',
                      width=900
                     )
        )
        self.filebrowser = pn.widgets.FileSelector(
            directory = os.path.join(os.getcwd(), 'exports'), 
            width=375, height=400
        )
        self.model_tabs = pn.Row(
            pn.Tabs(pn.pane.Markdown(self.return_README(),
                        name='README'
                    ),
                    pn.Column(
                        pn.pane.Markdown(
                            """### Configure \nHere's how to config."""
                        ),
                        pn.Tabs(
                            pn.Column(
                                pn.Row(
                                    self.file_selector, self.pointcloud_control
                                ),
                                self.axes3d,
                                name='Date'
                            ),
                            pn.Column(
                                pn.Row(self.raster_control, self.azi_bins,
                                       pn.WidgetBox(pn.Row(self.return_time_control,
                                                           self.horizon_preview
                                                          )
                                                   )
                                      ),
                                self.config_accordion,
                                name='Raster & Azimuth'
                            ),
                            pn.Column(
                                pn.Row(self.timeseries_control),
                                pn.WidgetBox(self.timeseries_dispatch, 
                                             name='Timeseries Plot Preview', 
                                             width=900
                                            ),
                                    name='Timeseries'
                            ),
                            pn.Column(
                                'Choose array format: .npy, .mat, .ascii',
                                name='Format',  width=900
                            )
                        ),
                        name='Configure'
                    ),
                    pn.Column(
                        pn.pane.Markdown(
                            """### Run \nHere's how you run."""
                        ),
                        pn.Row(
                            pn.Column(self.return_config_dict),
                            pn.Column(
                                pn.Row(self.return_run_button, 
                                       pn.Column(pn.Spacer(height=20),
                                                 self.progress)
                                      ),
                                self.return_log_pane
                                )
                        ),
                        name='Run'
                    ),
                    pn.Column(
                        pn.pane.Markdown(
                            """### Export \n Config your output, commit & review, then download."""
                        ),
                        pn.Tabs(
                            pn.Column(
                                'Heres the model',
                                self.video_dispatch,
                                name='Review'
                            ),
                            pn.Column(
                                '''Select which files you'd like, then download as zips''',
                                self.filebrowser,
                                name='Download'
                            )
                        ),
                        name='Export'
                    ),
                    active=0,
                    tabs_location='left'
                   ),
        )
        
        plt.close()
        return
        
    def dashboard(self):
        self.set_filename()
        self.set_dataframe()
        self.set_raster()
        self.update_config()
        self.set_controls()
        self.set_layout()
        self.horizon_package = self.slope2horz()
        return pn.Column(self.function_row,
                         self.model_tabs)