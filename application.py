#!/usr/bin/env python


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import sys

from parser import *
from term_parser import *
from natural_deduction_rules import *


class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Natural deduction", application=app)

        self.left_vbox = Gtk.VBox()
        self.vbox_texts = Gtk.VBox(spacing=0)
        self.vbox_texts.set_border_width(50)
        self.vbox_subgoals = Gtk.VBox()
        self.message_box = Gtk.HBox()
        self.message_box.set_border_width(50)
        self.middle_vbox = Gtk.VBox()
        self.middle_vbox.set_border_width(50)
        self.middle_vbox.set_size_request(200, 200)

        subgoals_label = Gtk.Label()
        subgoals_label.set_text('Subgoals: ')        
        self.middle_vbox.add(subgoals_label)
        
        self.resize(1200, 700)

        self.hbox = Gtk.HBox()

        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(20)
       
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_border_width(5)        
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.buffer1 = Gtk.TextBuffer()
        
        textview = Gtk.TextView(buffer=self.buffer1)
        textview.set_wrap_mode(Gtk.WrapMode.WORD)
        
        scrolled_window.add(textview)
        scrolled_window.set_size_request(300,200)

#==========================================================================================

        self.scrolled_window2 = Gtk.ScrolledWindow()
        self.scrolled_window2.set_border_width(5)
        self.scrolled_window2.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.buffer2 = Gtk.TextBuffer()
        
        self.textview2 = Gtk.TextView(buffer=self.buffer2)        
        self.textview2.set_wrap_mode(Gtk.WrapMode.WORD)
        
        self.scrolled_window2.add(self.textview2)
        self.scrolled_window2.set_size_request(300,200)

        self.middle_vbox.add(self.scrolled_window2)

        self.hbox_entries = Gtk.HBox()
        self.assumption_entry = Gtk.Entry()
        self.subgoal_entry = Gtk.Entry()
        self.term_entry = Gtk.Entry()

        self.right_label = Gtk.Label()
        self.right_label.set_text('Choose subgoal and assumption: ')

        self.middle_vbox.add(self.right_label)
        self.hbox_entries.add(self.subgoal_entry)
        self.hbox_entries.add(self.assumption_entry)
        self.middle_vbox.add(self.hbox_entries)
        

        self.btn1 = Gtk.RadioButton.new_with_label_from_widget(None, "Left")
        self.btn1.connect("toggled", self.on_selected)
        self.btn2 = Gtk.RadioButton.new_with_label_from_widget(self.btn1, "Right")
        self.btn2.connect("toggled", self.on_selected)

        self.middle_vbox.add(self.btn1)
        self.middle_vbox.add(self.btn2)

        self.term_label = Gtk.Label()
        self.term_label.set_text('Term for substitution: ')

        self.middle_vbox.add(self.term_label)
        self.middle_vbox.add(self.term_entry)

#=============================================================================================

        self.entry = Gtk.Entry()
               
        assumptions_label = Gtk.Label()
        assumptions_label.set_text('Assumptions: ')
        self.vbox_texts.add(assumptions_label)

        self.vbox_texts.add(scrolled_window)

        conclusion_label = Gtk.Label()
        conclusion_label.set_text('Conclusion: ')        
        self.vbox_texts.add(conclusion_label)        

        self.vbox_texts.add(self.entry)

        enter_button = Gtk.Button(label='Enter')
        enter_button.connect("clicked", self.enter_formulas)
        self.vbox_texts.add(enter_button)

        self.message = Gtk.Entry()
        msg_label = Gtk.Label()
        msg_label.set_text('Message: ')
        self.message_box.add(msg_label)
        self.message_box.add(self.message)

        self.left_vbox.add(self.vbox_texts)
        
        self.left_vbox.add(self.message_box)
        self.hbox.add(self.left_vbox)
        
        self.right_vbox = Gtk.VBox()  
        self.right_vbox.set_border_width(10)  
        self.right_vbox.add(self.grid)

 
        self.add_rules()
       
        
        self.hbox.add(self.right_vbox)
        self.hbox.add(self.middle_vbox)
        self.add(self.hbox)


    def add_rules(self):

        self.vbox_ci = Gtk.VBox()
        self.vbox_ce = Gtk.VBox()
        self.vbox_di = Gtk.VBox()
        self.vbox_de = Gtk.VBox()

        self.vbox_ei = Gtk.VBox()
        self.vbox_ee = Gtk.VBox()
        self.vbox_ui = Gtk.VBox()
        self.vbox_ue = Gtk.VBox()
        
        self.vbox_ni = Gtk.VBox()
        self.vbox_ne = Gtk.VBox()
        self.vbox_ii = Gtk.VBox()
        self.vbox_ie = Gtk.VBox()
                

        image_ci = Gtk.Image()
        image_ci.set_from_file('resources/conjI.png')        
        self.button_ci = Gtk.Button(label='Conjunction introduction')
        self.vbox_ci.add(image_ci)
        self.vbox_ci.add(self.button_ci)
        self.grid.attach(self.vbox_ci, 0, 0, 10, 10)
        
        image_ce = Gtk.Image()
        image_ce.set_from_file('resources/conjE.png')
        self.button_ce = Gtk.Button(label='Conjunction elimination')
        self.vbox_ce.add(image_ce)
        self.vbox_ce.add(self.button_ce)
        self.grid.attach(self.vbox_ce, 10, 0, 10, 10)

        image_di = Gtk.Image()
        image_di.set_from_file('resources/disjI.png')
        self.button_di = Gtk.Button(label='Disjunctiom introduction')
        self.vbox_di.add(image_di)
        self.vbox_di.add(self.button_di)
        self.grid.attach(self.vbox_di, 0, 10, 10, 10)
        
        image_de = Gtk.Image()
        image_de.set_from_file('resources/disjE.png')
        self.button_de = Gtk.Button(label='Disjunctiom elimination')
        self.vbox_de.add(image_de)
        self.vbox_de.add(self.button_de)
        self.grid.attach(self.vbox_de, 10, 10, 10, 10)
        
        
        image_ii = Gtk.Image()
        image_ii.set_from_file('resources/impI.png')
        self.button_ii = Gtk.Button(label='Implication introduction')
        self.vbox_ii.add(image_ii)
        self.vbox_ii.add(self.button_ii)
        self.grid.attach(self.vbox_ii, 0, 20, 10, 10)
        
        image_ie = Gtk.Image()
        image_ie.set_from_file('resources/impE.png')
        self.button_ie = Gtk.Button(label='Implication elimination')
        self.vbox_ie.add(image_ie)
        self.vbox_ie.add(self.button_ie)
        self.grid.attach(self.vbox_ie, 10, 20, 10, 10)

        image_ni = Gtk.Image()
        image_ni.set_from_file('resources/notI.png')
        self.button_ni = Gtk.Button(label='Negation introduction')
        self.vbox_ni.add(image_ni)
        self.vbox_ni.add(self.button_ni)
        self.grid.attach(self.vbox_ni, 0, 30, 10, 10)
        
        image_ne = Gtk.Image()
        image_ne.set_from_file('resources/notE.png')
        self.button_ne = Gtk.Button(label='Negation elimination')
        self.vbox_ne.add(image_ne)
        self.vbox_ne.add(self.button_ne)
        self.grid.attach(self.vbox_ne, 10, 30, 10, 10)

        image_ui = Gtk.Image()
        image_ui.set_from_file('resources/allI.png')
        self.button_ui = Gtk.Button(label='Universal introduction')
        self.vbox_ui.add(image_ui)
        self.vbox_ui.add(self.button_ui)
        self.grid.attach(self.vbox_ui, 20, 0, 10, 10)
        
        image_ue = Gtk.Image()
        image_ue = Gtk.Image()
        image_ue.set_from_file('resources/allE.png')
        self.button_ue = Gtk.Button(label='Universal elimination')
        self.vbox_ue.add(image_ue)
        self.vbox_ue.add(self.button_ue)
        self.grid.attach(self.vbox_ue, 20, 10, 10, 10)
        
        image_ei = Gtk.Image()
        image_ei.set_from_file('resources/exisI.png')
        self.button_ei = Gtk.Button(label='Existential introduction')
        self.vbox_ei.add(image_ei)
        self.vbox_ei.add(self.button_ei)
        self.grid.attach(self.vbox_ei, 20, 20, 10, 10)

        image_ee = Gtk.Image()
        image_ee.set_from_file('resources/exisE.png')
        self.button_ee = Gtk.Button(label='Existential elimination')
        self.vbox_ee.add(image_ee)
        self.vbox_ee.add(self.button_ee)
        self.grid.attach(self.vbox_ee, 20, 30, 10, 10)
        
        self.assumption_button = Gtk.Button(label='Assumption')
        self.right_vbox.add(self.assumption_button)

        self.button_ci.connect("clicked", self.ci_rule)
        self.button_ce.connect("clicked", self.ce_rule)
        self.button_di.connect("clicked", self.di_rule)
        self.button_de.connect("clicked", self.de_rule)
        self.button_ii.connect("clicked", self.ii_rule)
        self.button_ie.connect("clicked", self.ie_rule)
        self.button_ni.connect("clicked", self.ni_rule)
        self.button_ne.connect("clicked", self.ne_rule)
        self.button_ui.connect("clicked", self.ui_rule)
        self.button_ue.connect("clicked", self.ue_rule)
        self.button_ei.connect("clicked", self.ei_rule)
        self.button_ee.connect("clicked", self.ee_rule)

        self.assumption_button.connect('clicked', self.asmp_rule)


    def enter_formulas(self, widget):

        start_iter = self.buffer1.get_start_iter()
        end_iter = self.buffer1.get_end_iter()
        
    
        assumptions_text = self.buffer1.get_text(start_iter, end_iter, True)
        assumptions = []
        for line in assumptions_text.splitlines():
            assumptions.append(parse(line))
        
        conclusion = parse(self.entry.get_text())

        subgoals.append(Theorem(assumptions, conclusion))


        self.buffer2.set_text(str_subgoals())

        
    def on_selected(self, button):
        
        if button.get_active():
            return True
        else:
            return False

    
    def ci_rule(self, widget):

        subgoal_idx = int(self.subgoal_entry.get_text())
    
        success = conjunction_introduction(subgoals[subgoal_idx - 1])

        if(not success):
            self.message.set_text('Rule cannot be applied.')

        else:
            self.buffer2.set_text(str_subgoals())
            self.message.set_text('Conjunction introduction applied.')
            


    def ce_rule(self, widget):
        assumption_idx = int(self.assumption_entry.get_text())
        subgoal_idx = int(self.subgoal_entry.get_text())
    
        if self.btn1.get_active():
            success = conjunction_elimination_left(subgoals[subgoal_idx - 1], subgoals[subgoal_idx - 1].assumptions[assumption_idx - 1])
        else:
            success = conjunction_elimination_right(subgoals[subgoal_idx - 1], subgoals[subgoal_idx - 1].assumptions[assumption_idx - 1])
        
        if(not success):
            self.message.set_text('Rule cannot be applied.')

        else:
            self.buffer2.set_text(str_subgoals())
            self.message.set_text('Conjunction elimination applied.')


    def di_rule(self, widget):

        subgoal_idx = int(self.subgoal_entry.get_text())
    
        if self.btn1.get_active():
            success = disjunction_introduction_left(subgoals[subgoal_idx - 1])
        else:
            success = disjunction_introduction_right(subgoals[subgoal_idx - 1])
        

        if(not success):
            self.message.set_text('Rule cannot be applied.')

        else:
            self.buffer2.set_text(str_subgoals())
            self.message.set_text('Disjunction introduction applied.')


    def de_rule(self, widget):

        assumption_idx = int(self.assumption_entry.get_text())
        subgoal_idx = int(self.subgoal_entry.get_text())
    
        success = disjunction_elimination(subgoals[subgoal_idx - 1], subgoals[subgoal_idx - 1].assumptions[assumption_idx - 1])
        
        if(not success):
            self.message.set_text('Rule cannot be applied.')

        else:
            self.buffer2.set_text(str_subgoals())
            self.message.set_text('Disjunction elimination applied.')


    def ii_rule(self, widget):

        subgoal_idx = int(self.subgoal_entry.get_text())
    
        success = implication_introduction(subgoals[subgoal_idx - 1])

        if(not success):
            self.message.set_text('Rule cannot be applied.')

        else:
            self.buffer2.set_text(str_subgoals())
            self.message.set_text('Implication introduction applied.')


    def ie_rule(self, widget):

        assumption_idx = int(self.assumption_entry.get_text())
        subgoal_idx = int(self.subgoal_entry.get_text())

    
        success = modus_ponens(subgoals[subgoal_idx - 1], subgoals[subgoal_idx - 1].assumptions[assumption_idx - 1])
        
        if(not success):
            self.message.set_text('Rule cannot be applied.')

        else:
            self.buffer2.set_text(str_subgoals())
            self.message.set_text('Implication elimination applied.')


    def ni_rule(self, widget):
        subgoal_idx = int(self.subgoal_entry.get_text())
    
        success = negation_introduction(subgoals[subgoal_idx - 1])

        if(not success):
            self.message.set_text('Rule cannot be applied.')

        else:
            self.buffer2.set_text(str_subgoals())
            self.message.set_text('Negation introduction applied.')

    def ne_rule(self, widget):

        assumption_idx = int(self.assumption_entry.get_text())
        subgoal_idx = int(self.subgoal_entry.get_text())

    
        success = negation_elimination(subgoals[subgoal_idx - 1], subgoals[subgoal_idx - 1].assumptions[assumption_idx - 1])
        
        if(not success):
            self.message.set_text('Rule cannot be applied.')

        else:
            self.buffer2.set_text(str_subgoals())
            self.message.set_text('Negation elimination applied.')


    def ui_rule(self, widget):

        subgoal_idx = int(self.subgoal_entry.get_text())
    
        success = universal_introduction(subgoals[subgoal_idx - 1])

        if(not success):
            self.message.set_text('Rule cannot be applied.')

        else:
            self.buffer2.set_text(str_subgoals())
            self.message.set_text('Universal introduction applied.')


    def ue_rule(self, widget):

        assumption_idx = int(self.assumption_entry.get_text())
        subgoal_idx = int(self.subgoal_entry.get_text())
        term = parse_term(self.term_entry.get_text())

    
        success = universal_elimination(subgoals[subgoal_idx - 1], subgoals[subgoal_idx - 1].assumptions[assumption_idx - 1], term)
        
        if(not success):
            self.message.set_text('Rule cannot be applied.')

        else:
            self.buffer2.set_text(str_subgoals())
            self.message.set_text('Universal elimination applied.')

    def ei_rule(self, widget):

        subgoal_idx = int(self.subgoal_entry.get_text())
        term = parse_term(self.term_entry.get_text())
    
        success = existential_introduction(subgoals[subgoal_idx - 1], term)

        if(not success):
            self.message.set_text('Rule cannot be applied.')

        else:
            self.buffer2.set_text(str_subgoals())
            self.message.set_text('Existential introduction applied.')


    def ee_rule(self, widget):

        assumption_idx = int(self.assumption_entry.get_text())
        subgoal_idx = int(self.subgoal_entry.get_text())
        term = parse_term(self.term_entry.get_text())
    
        success = existential_elimination(subgoals[subgoal_idx - 1], subgoals[subgoal_idx - 1].assumptions[assumption_idx - 1])
        
        if(not success):
            self.message.set_text('Rule cannot be applied.')

        else:
            self.buffer2.set_text(str_subgoals())
            self.message.set_text('Existential elimination applied.')

    def asmp_rule(self, widget):

        subgoal_idx = int(self.subgoal_entry.get_text())

        success = apply_assumption(subgoals[subgoal_idx - 1])

        if(not success):
            self.message.set_text('Rule cannot be applied.')

        else:
            self.buffer2.set_text(str_subgoals())
            self.message.set_text('Assumption applied.')


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
app = MyWindow()
exit_status = app.run(sys.argv)
sys.exit(exit_status)

