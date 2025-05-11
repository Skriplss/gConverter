import wx

class TabManager:
    def __init__(self, main_frame):
        self.main_frame = main_frame
        self.converter_tab_locked = False
    
    def block_converter_tab(self):
        self.converter_tab_locked = True
    
    def unblock_converter_tab(self):
        self.converter_tab_locked = False
    
    def is_converter_tab_locked(self):
        return self.converter_tab_locked
    
    def handle_tab_change(self, event):
        old_selection = event.GetOldSelection()
        new_selection = event.GetSelection()
        current_selection = self.main_frame.notebook_main.GetSelection()
        
        page_count = self.main_frame.notebook_main.GetPageCount()
        
        target_tab_name = ""
        if 0 <= new_selection < page_count:
            target_tab_name = self.main_frame.notebook_main.GetPageText(new_selection)
        
        if old_selection == new_selection:
            if current_selection == 0:
                target_tab_name = "Vizualizácia"
            else:
                target_tab_name = "Konverzia kódu"
        
        if target_tab_name == "Vizualizácia":
            rapid_text = self.main_frame.rapid_output.GetValue()
            if not rapid_text or rapid_text.strip() == "":
                wx.MessageBox("Najprv konvertujte G-kód do RAPID pre vizualizáciu", 
                              "Upozornenie", wx.OK | wx.ICON_WARNING)
                return False
        
        elif target_tab_name == "Konverzia kódu" and self.converter_tab_locked:
            wx.MessageBox("Počas vizualizácie nemožno pristupovať k záložke konvertora", 
                          "Upozornenie", wx.OK | wx.ICON_WARNING)
            return False
        
        return True


_tab_manager = None

def init_tab_manager(main_frame):
    global _tab_manager
    _tab_manager = TabManager(main_frame)
    return _tab_manager

def get_tab_manager():
    global _tab_manager
    if _tab_manager is None:
        raise RuntimeError("TabManager nie je inicializovaný")
    return _tab_manager 