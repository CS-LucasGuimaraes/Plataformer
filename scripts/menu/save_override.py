import json
from scripts.utils import json_dump
from scripts.menu.utils import Button, Panel
from game import Game
from scripts.menu.character_selection import character_selection

class save_override(character_selection):
    def __init__(self, main_menu, joysticks):
        super().__init__(main_menu, joysticks)

    def json_dump(self, save):
        f = open('saves/'+str(save)+'.json', 'w')
        json.dump({
                    "current_level": 1,
                    "current_hearts": 3,
                    "current_collectibles": 
                        {
                            "key": 0,
                            "coin": 0,
                            "diamond": 0
                            }
                    }, f)
        f.close()
        
    def render_panels(self, surf, m_pos, clicking):
        if self.p1.update(surf, m_pos, clicking):
            self.json_dump(1)
        
        if self.p2.update(surf, m_pos, clicking):
            self.json_dump(2)
        
        if self.p3.update(surf, m_pos, clicking):
            self.json_dump(3)
        
        if self.p4.update(surf, m_pos, clicking):
            self.json_dump(4)

        return super().render_panels(surf, m_pos, clicking)
    
    def render(self, surf, m_pos, clicking):
        return super().render(surf, m_pos, clicking, override=True)