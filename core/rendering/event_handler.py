class EventHandler:
    ANIMATION_SPEED_OPTIONS = {
        0: 70,  # x0.5
        1: 50,  # x1
        2: 25,  # x2
        3: 10,  # x5
        4: 5    # x10
    }
    
    def __init__(self, plot_manager, animation_manager, rotation_matrix):
        self.plot_manager = plot_manager
        self.animation_manager = animation_manager
        self.rotation_matrix = rotation_matrix
    
    def on_size(self, event):
        self.plot_manager.canvas.draw()
        event.Skip()
    
    def on_show(self, event):
        if not event.IsShown():
            self.animation_manager.stop_visualize()
        event.Skip() 
        
    def on_mode_change(self, event, mode_choice, visualize_button, stop_button):
        selection = mode_choice.GetSelection()
        event.Skip()

        if selection == 0:
            visualize_button.Enable(True)
            stop_button.Enable(True)
            return "animated"
        else:
            visualize_button.Enable(False)
            stop_button.Enable(False)
            return "immediate"
            
    def on_speed_change(self, speed_choice, event):
        selection = speed_choice.GetSelection()
        interval = self.ANIMATION_SPEED_OPTIONS.get(selection, self.ANIMATION_SPEED_OPTIONS[1])
        self.animation_manager.set_animation_interval(interval)
        if event is not None:
            event.Skip()