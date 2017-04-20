#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import re

class Rule:
    ''' Создан для хранения правил '''
    def __init__(self, name, condition, result):
        self.name = name
        self.condition = condition
        self.result = result

class ExpertSysModel:
    ''' Хранение данных и операций по обработке данных '''
    def __init__(self):
        self.rules = list()
        self.states = list()
        self.results = dict()

    def add_rule(self, name, condition, result):
        self.rules.append(
            Rule(name, condition, result)
        )

    def edit_rule(self, num, name, condition, result):
        self.rules[num] = Rule(name, condition, result)

    def get_rules_amount(self):
        return len(self.rules)

    def add_state(self, state):
        self.states.append(state)

    def edit_state(self, num, state):
        self.states[num] = state

    def get_states_amount(self):
        return len(self.states)

    def add_result(self, rule_name, conclusions):
        self.results[rule_name] = conclusions

    def get_results_amount(self):
        return len(self.results)


class ExpertSysController:
    ''' Управления функциями МОДЕЛИ. Данные методы вызываются из ВИДА '''
    def __init__(self, model=None):
        self.model = model
        self.rule_view = None
        self.cond_view = None
        self.rule_edit_mode = False
        self.state_edit_mode = False
        self.edit_num = None

    def set_view(self, rule_view=None, state_view=None):
        if rule_view:
            self.rule_view = rule_view
        if state_view:
            self.state_view = state_view

    def add_new_rule(self):
        ''' добавление нового правила в МОДЕЛЬ '''
        name = self.rule_view.name_var.get()
        condition = self.rule_view.conditions_var.get()
        result = self.rule_view.result_var.get()
        if name and condition and result:
            if self.rule_edit_mode:
                self.model.edit_rule(self.rule_edit_num-1, name, condition, result)
                self.rule_edit_mode = False
                self.rule_view.name_var.set('')
                self.rule_view.conditions_var.set('')
                self.rule_view.result_var.set('')
                self.rule_view.refresh_rules()
            elif condition not in [rule.condition for rule in self.model.rules]:
                self.model.add_rule(name, condition, result)
                self.rule_view.name_var.set('')
                self.rule_view.conditions_var.set('')
                self.rule_view.result_var.set('')
                self.rule_view.refresh_rules()
            else:
                mes = 'Правило c данными условиями уже есть в системе.\nНазвание: {}'
                self.rule_view.ok_message(mes.format(name))

    def del_rule(self):
        num = int(self.rule_view.select_rule_num_var.get())
        if num:
            del self.model.rules[num-1]
            self.rule_view.refresh_rules()

    def edit_rule(self):
        num = int(self.rule_view.select_rule_num_var.get())
        if num:
            self.rule_edit_mode = True
            self.rule_edit_num = num
            cond = self.model.rules[num-1].condition
            name = self.model.rules[num-1].name
            res = self.model.rules[num-1].result
            self.rule_view.name_var.set(name)
            self.rule_view.conditions_var.set(cond)
            self.rule_view.result_var.set(res)
            self.rule_view.refresh_rules()

    def save_rules_to_file(self, file):
        for num, rule in enumerate(self.model.rules):
            line = '{num}) ПРАВИЛО {name} ЕСЛИ {cond} ТО {res}.'.format(
                num=num+1,
                name=rule.name,
                cond=rule.condition,
                res=rule.result)
            print(line, file=file)
        file.close()

    def load_rules_from_file(self, file):
        rule_re = re.compile(r'\d{1,2}\) ПРАВИЛО (?P<name>.+) ЕСЛИ (?P<cond>.+) ТО (?P<res>.+)\.')
        self.model.rules = []
        for line in file:
            match = rule_re.match(line)
            if match:
                name = match.group('name')
                condition = match.group('cond')
                result = match.group('res')
                self.model.add_rule(name, condition, result)
            else:
                print('Ошибка! Очередная строка не соответствует шаблону.\n"{}"'.format(line))
        file.close()
        self.rule_view.refresh_rules()

    def add_new_state(self):
        ''' добавление нового состояния в МОДЕЛЬ '''
        state = self.state_view.state_var.get()
        if state:
            if self.state_edit_mode:
                self.model.edit_state(self.state_edit_num-1, state)
                self.state_edit_mode = False
                self.state_view.state_var.set('')
                self.state_view.refresh_states()
            elif state.lower() not in self.model.states:
                self.state_view.state_var.set('')
                self.model.add_state(state.lower())
                self.state_view.refresh_states()
            else:
                self.state_view.ok_message('Состояние "{}" уже есть в системе'.format(state))
                self.state_view.state_var.set('')

    def del_state(self):
        num = int(self.state_view.select_state_num_var.get())
        if num:
            del self.model.states[num-1]
            self.state_view.refresh_states()

    def edit_state(self):
        num = int(self.state_view.select_state_num_var.get())
        if num:
            self.state_edit_mode = True
            self.state_edit_num = num
            state = self.model.states[num - 1]
            self.state_view.state_var.set(state)
            self.state_view.refresh_states()

    def save_states_to_file(self, file):
        for num, state in enumerate(self.model.states):
            line = '{0}) {1}.'.format(num+1, state)
            print(line, file=file)
        file.close()

    def load_states_from_file(self, file):
        state_re = re.compile(r'\d{1,2}\) (?P<state>.+)\.')
        self.model.states = []
        for line in file:
            match = state_re.match(line)
            if match:
                state = match.group('state')
                self.model.add_state(state)
            else:
                print('Ошибка! Очередная строка не соответствует шаблону.\n"{}"'.format(line))
        file.close()
        self.state_view.refresh_states()

    def save_result_to_file(self, file):
        for num_rule, rule in enumerate(self.model.results.keys()):
            print('{}. {}'.format(num_rule + 1, rule), file=file)
            for num_res, result in enumerate(self.model.results[rule]):
                print('{}) {}'.format(num_res+1, result), file=file)
            print(file=file)
        file.close()

    def start_processing(self):
        self.model.add_result('УК РФ, гл.1, ст.1, п.2',
                               ['штраф 100, 300',
                                'штраф в размере заработной платы 12, 24',
                                'исправительные работы 12, 24',
                                'лишение свободы 48',
                                'ограничение свободы 48',
                                'принудительные работы 48'])
        self.model.add_result('УК РФ, гл.1, ст.1, п.1',
                               ['штраф 200',
                                'штраф в размере заработной платы до 18',
                                'лишение свободы 24',
                                'исправительные работы 12',
                                'ограничение свободы 24',
                                'принудительные работы 24'])
        self.state_view.refresh_results()

    def clear_results(self):
        self.model.results = dict()
        self.state_view.refresh_results()


class RulesView(Frame):
    ''' Интерфейс для управления созданием и отображением ПРАВИЛ'''
    def __init__(self, model=None, controller=None, master=None, **config):
        self.model = model
        self.controller = controller
        self.controller.set_view(rule_view=self)
        super().__init__(master)
        self.configure(bg='black')
        self.pack(side='left', expand='yes', fill='both', padx=5, pady=5)
        self.create_widgets(**config)

    def create_widgets(self, **config):
        # delete|edit
        frame_delete = Frame(self)
        self.delete_but = Button(frame_delete,
                                 bd=3,
                                 text='Удалить',
                                 bg='#eebebe',
                                 command=self.controller.del_rule,
                                 state='disabled',
                                 **config)
        self.edit_but = Button(frame_delete,
                                 bd=3,
                                 text='Изменить',
                                 bg='#bebeee',
                                 command=self.controller.edit_rule,
                                 state='disabled',
                                 **config)
        self.select_rule_num_var = StringVar(0)
        self.del_edit_spinbox = Spinbox(frame_delete,
                                        width=5,
                                        from_=0, to=0,
                                        textvariable=self.select_rule_num_var,
                                        state='disabled',
                                        **config)
        # delete|edit packed
        frame_delete.pack(side='top', fill='x')
        Label(frame_delete, text='Номер правила:', **config).pack(side='left', padx=5)
        self.delete_but.pack(side='right', padx=5, pady=5)
        self.edit_but.pack(side='right', padx=5, pady=5)
        self.del_edit_spinbox.pack(side='right', fill='y', pady=5)

        # rules in text widget
        frame_text_parent = Frame(self)
        frame_text_child = Frame(frame_text_parent)
        self.rules_txt = Text(frame_text_child,
                              width=40,
                              height=15,
                              wrap='word',
                              state='disabled',
                              **config)
        scrollbar = Scrollbar(frame_text_child,
                              command=self.rules_txt.yview)
        self.rules_txt.config(yscrollcommand=scrollbar.set)
        # text packed
        frame_text_parent.pack(side='top', fill='both', expand=True)
        frame_text_child.pack(padx=5, fill='both', expand=True)
        self.rules_txt.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='left', fill='y')

        # add
        frame_add_parent = Frame(self)
        frame_add_child = Frame(frame_add_parent)

        self.name_var = StringVar()
        name_ent = Entry(frame_add_child,
                               textvariable=self.name_var,
                               fg='grey',
                               **config)
        self.conditions_var = StringVar()
        conditions_ent = Entry(frame_add_child,
                               textvariable=self.conditions_var,
                               fg='grey',
                               **config)
        self.result_var = StringVar()
        result_ent = Entry(frame_add_child,
                           textvariable=self.result_var,
                           fg='grey',
                           **config)
        self.add_rules_but = Button(frame_add_parent,
                               bd=3,
                               text="Добавить",
                               bg='#bed6be',
                               command=self.controller.add_new_rule,
                               **config)
        # add packed
        frame_add_parent.pack(side='top', fill='x')
        frame_add_child.pack(side='left', fill='x', expand=True, padx=5)
        Label(frame_add_child, text="Наименование:", **config).pack(anchor=W,)
        name_ent.pack(fill='x')
        Label(frame_add_child, text="Условия:", **config).pack(anchor=W)
        conditions_ent.pack(fill='x')
        Label(frame_add_child, text="Результат:", **config).pack(anchor=W)
        result_ent.pack(fill='x')
        self.add_rules_but.pack(side='right', fill='both', padx=5, pady=5)

        # load|safe
        frame_loadsave = Frame(self)
        load_but = Button(frame_loadsave,
                          bd=3,
                          text='Загрузить',
                          bg='#ffddaa',
                          command=self.load_rules,
                          **config)
        self.save_but = Button(frame_loadsave,
                          bd=3,
                          text='Сохранить',
                          bg='#ffddaa',
                          state='disabled',
                          command=self.save_rules,
                          **config)
        # load|safe packed
        frame_loadsave.pack(side='top', fill='x')
        load_but.pack(side='left', fill='x', expand=True,  padx=5, pady=5)
        self.save_but.pack(side='right', fill='x', expand=True, padx=5, pady=5)

    def ok_message(self, message):
        messagebox.showinfo('Ошибка', message)

    def refresh_rules(self):
        ''' Обновляет список правил в соответствии с моделью '''
        on_off_widgets = [self.del_edit_spinbox,
                          self.delete_but,
                          self.edit_but,
                          self.save_but]
        if self.model.get_rules_amount() > 0:
            for widget in on_off_widgets:
                widget.config(state='normal')
            if self.controller.rule_edit_mode:
                self.add_rules_but.config(text='Редиктировать')
            else:
                self.add_rules_but.config(text='Добавить')
            self.del_edit_spinbox.config(from_=1, to=self.model.get_rules_amount())
            self.select_rule_num_var.set(1)
            self.rules_txt.config(state='normal')
            self.rules_txt.delete('1.0', END)
            template = '{num}) ПРАВИЛО {name}\nЕСЛИ {condition}\nТО {result}\n\n'
            for num, rule in enumerate(self.model.rules):
                line = template.format(num=num+1,
                                       name=rule.name,
                                       condition=rule.condition,
                                       result=rule.result)
                self.rules_txt.insert('{0}.{1}'.format(num*4+1, 0), line)
            self.rules_txt.config(state='disabled')
            self.rules_txt.see('{0}.{1}'.format(num+1, 0))
            if self.model.get_states_amount() > 0:
                self.controller.state_view.start_but.config(state='normal')
        else:
            for widget in on_off_widgets + [self.controller.state_view.start_but]:
                widget.config(state='disabled')
            self.select_rule_num_var.set(0)
            self.del_edit_spinbox.config(from_=0, to=0)
            self.rules_txt.config(state='normal')
            self.rules_txt.delete('1.0', END)
            self.rules_txt.config(state='disabled')

    def save_rules(self):
        if self.model.rules:
            file_var = filedialog.asksaveasfile(mode='w',
                                                defaultextension=".rules",
                                                filetypes=[('rules files', '.rules'), ('all files', '.*')],
                                                title="Сохранение условий. Введите имя файла.")
            if file_var:
                self.controller.save_rules_to_file(file_var)

    def load_rules(self):
        filename = filedialog.askopenfilename(filetypes=[('*.rules files', '*.rules')])
        if filename:
            file_var = open(filename, 'r')
            self.controller.load_rules_from_file(file_var)


class StatesView(Frame):
    ''' Интерфейс для управления созданием и отображением СОСТОЯНИЙ и РЕЗУЛЬТАТОВ'''
    def __init__(self, model=None, controller=None, master=None, **config):
        self.model = model
        self.controller = controller
        self.controller.set_view(state_view=self)
        super().__init__(master)
        self.configure(bg='black')
        self.pack(side='left', expand='yes', fill='both', padx=5, pady=5)
        self.create_state_widgets(**config)
        self.create_result_widgets(**config)

    def create_state_widgets(self, **config):
        # add states with entry & button
        frame_add_parent = Frame(self)
        frame_add_child = Frame(frame_add_parent)
        self.state_var = StringVar()
        state_ent = Entry(frame_add_child,
                               textvariable=self.state_var,
                               fg='grey',
                               **config)
        self.state_add_but = Button(frame_add_parent,
                               width=9, bd=3,
                               text='Добавить',
                               bg='#bed6be',
                               command=self.controller.add_new_state,
                               **config)
        # PACKED add states with entry, scroll & button
        frame_add_parent.pack(side='top', fill='x')
        frame_add_child.pack(side='left', expand=True, fill='x', pady=5, padx=5)
        Label(frame_add_child, text="Состояние:", **config).pack(anchor=W)
        state_ent.pack(fill='x')
        self.state_add_but.pack(side='right', fill='both', pady=5, padx=5)

        # state text with opportunity to delete and edit (spinbox & 2 buttons),
        # save & load buttons
        frame_state_parent = Frame(self)
        frame_state_child = Frame(frame_state_parent)
        self.states_txt = Text(frame_state_child,
                               width=20,
                               height=12,
                               wrap='word',
                               state='disabled',
                               **config)
        states_scrollbar = Scrollbar(frame_state_child, command=self.states_txt.yview)
        self.states_txt.config(yscrollcommand=states_scrollbar.set)
        self.select_state_num_var = StringVar(0)
        self.del_edit_states_spinbox = Spinbox(frame_state_parent,
                                               width=5,
                                               from_=0, to=0,
                                               textvariable=self.select_state_num_var,
                                               state='disabled',
                                               **config)
        self.states_del_but = Button(frame_state_parent,
                                     width=9,
                                     text='Удалить',
                                     bg='#eebebe',
                                     state='disabled',
                                     command=self.controller.del_state,
                                     **config)
        self.states_edit_but = Button(frame_state_parent,
                                      width=9,
                                      text='Изменить',
                                      bg='#bebeee',
                                      state='disabled',
                                      command=self.controller.edit_state,
                                      **config)
        self.save_states_but = Button(frame_state_parent,
                                      width=9, bd=3,
                                      text='Сохранить',
                                      bg='#ffddaa',
                                      state='disabled',
                                      command=self.save_states,
                                      **config)
        load_states_but = Button(frame_state_parent,
                                 width=9, bd=3,
                                 text='Загрузить',
                                 bg='#ffddaa',
                                 command=self.load_states,
                                 **config)
        # PACKED conditions text with opportunity to delete (spinbox & button),
        # save & load buttons
        frame_state_parent.pack(side='top', fill='x', anchor=N)
        frame_state_child.pack(side='left', expand=True, fill='both', pady=5, padx=5)
        self.states_txt.pack(side='left', expand=True, fill='both', pady=5)
        states_scrollbar.pack(side='left', fill='y', pady=5)
        self.del_edit_states_spinbox.pack(side='top',fill='x', pady=5, padx=5)
        self.states_del_but.pack(side='top', fill='x', pady=5, padx=5)
        self.states_edit_but.pack(side='top', fill='x', pady=5, padx=5)
        self.save_states_but.pack(side='top', fill='x', expand=True, anchor='s', pady=5, padx=5)
        load_states_but.pack(side='bottom', fill='x', pady=5, padx=5)

    def create_result_widgets(self, **config):
        # result text, start button, save result button
        frame_result_parent = Frame(self)
        frame_result_child_txt = Frame(frame_result_parent)
        frame_result_child_btn = Frame(frame_result_parent)
        self.result_txt = Text(frame_result_child_txt,
                               width=35,
                               height=8,
                               state='disabled',
                               wrap='word',
                               **config)
        result_scrollbar = Scrollbar(frame_result_child_txt, command=self.result_txt.yview)
        self.result_txt.config(yscrollcommand=result_scrollbar.set)
        self.start_but = Button(frame_result_child_btn,
                                bd=3,
                                text='РЕШИТЬ',
                                bg='black',
                                fg='white',
                                state='disabled',
                                command=self.controller.start_processing,
                                **config)
        self.save_result_but = Button(frame_result_child_btn,
                                      bd=3,
                                      text='Сохранить',
                                      bg='#ffddaa',
                                      state='disabled',
                                      command=self.save_result,
                                      **config)
        self.clear_result_but = Button(frame_result_child_btn,
                                       bd=3,
                                       text='Очистить',
                                       bg='#eebebe',
                                       state='disabled',
                                       command=self.clear_result,
                                       **config)
        # PACKED result text, start button, save result button
        Label(frame_result_parent, text='Результаты:', **config).pack(side='top', padx=5, anchor=W)
        frame_result_parent.pack(side='top', fill='both', expand=True)
        frame_result_child_txt.pack(side='top', fill='both', expand=True, padx=5)
        self.result_txt.pack(side='left', fill='both', expand=True)
        result_scrollbar.pack(side='left', fill='y')
        frame_result_child_btn.pack(side='bottom', fill='both')
        self.save_result_but.pack(side='left', expand=True, fill='x', pady=5, padx=5)
        self.clear_result_but.pack(side='left', expand=True, fill='x', pady=5, padx=5)
        self.start_but.pack(side='right', expand=True, fill='x', pady=5, padx=5)

    def ok_message(self, message):
        messagebox.showinfo('Ошибка', message)

    def refresh_states(self):
        ''' Обновляет список состояний в соответствии с моделью '''
        on_off_widgets = [self.del_edit_states_spinbox,
                          self.states_del_but,
                          self.states_edit_but,
                          self.save_states_but]
        if self.model.get_states_amount() > 0:
            for widget in on_off_widgets:
                widget.config(state='normal')
            self.state_add_but.config(text='Редактир' if self.controller.state_edit_mode else 'Добавить')
            self.del_edit_states_spinbox.config(from_=1, to=self.model.get_states_amount())
            self.select_state_num_var.set(1)
            self.states_txt.config(state='normal')
            self.states_txt.delete('1.0', END)
            for num, state in enumerate(self.model.states):
                line = '{num}) {state}\n'.format(num=num+1, state=state)
                self.states_txt.insert('{0}.{1}'.format(num+1, 0), line)
            self.states_txt.config(state='disable')
            self.states_txt.see('{0}.{1}'.format(num+1, 0))
            if self.model.get_rules_amount() > 0:
                self.start_but.config(state='normal')
        else:
            for widget in on_off_widgets + [self.start_but]:
                widget.config(state='disable')
            self.select_state_num_var.set(0)
            self.del_edit_states_spinbox.config(from_=0, to=0)
            self.states_txt.config(state='normal')
            self.states_txt.delete('1.0', END)
            self.states_txt.config(state='disable')

        if self.model.get_results_amount() > 0:
            self.save_result_but.config(state='normal')
            self.clear_result_but.config(state='normal')
        else:
            self.save_result_but.config(state='disable')
            self.clear_result_but.config(state='disable')

    def refresh_results(self):
        self.result_txt.config(state='normal')
        self.result_txt.delete('1.0', END)
        on_off_widgets = [self.save_result_but, self.clear_result_but]
        if self.model.get_results_amount() > 0:
            for widget in on_off_widgets:
                widget.config(state='normal')
            line_num = 1
            for num_rule, rule in enumerate(self.model.results.keys()):
                self.result_txt.insert('{}.{}'.format(line_num, 0),
                                                  str(num_rule+1)+'. '+rule+'\n')
                line_num += 1
                for num_res, result in enumerate(self.model.results[rule]):
                    self.result_txt.insert('{}.{}'.format(line_num, 0),
                                                      str(num_res + 1)+') '+result+'\n')
                    line_num += 1
                self.result_txt.insert('{}.{}'.format(line_num, 0), '\n')
                line_num += 1
        else:
            for widget in on_off_widgets:
                widget.config(state='disabled')
        self.result_txt.config(state='disabled')

    def save_states(self):
        if self.model.get_states_amount() > 0:
            file_var = filedialog.asksaveasfile(mode='w',
                                                defaultextension=".states",
                                                filetypes=[('states files', '.states'), ('all files', '.*')],
                                                title="Сохранение состояния. Введите имя файла.")
            if file_var:
                self.controller.save_states_to_file(file_var)

    def load_states(self):
        filename = filedialog.askopenfilename(filetypes=[('*.states files', '*.states')])
        if filename:
            file_var = open(filename, 'r')
            self.controller.load_states_from_file(file_var)

    def save_result(self):
        if self.model.get_results_amount() > 0:
            file_var = filedialog.asksaveasfile(mode='w',
                                                defaultextension=".results",
                                                filetypes=[('results files', '.results'), ('all files', '.*')],
                                                title="Сохранение результата. Введите имя файла.")
            if file_var:
                self.controller.save_result_to_file(file_var)

    def clear_result(self):
        self.controller.clear_results()


expert_sys_model = ExpertSysModel()
expert_sys_controller = ExpertSysController(expert_sys_model)

root = Tk()
root.title('Экспертная система')
root.config(bg='grey')
root.geometry('880x625+100+100')
root.minsize(width=481, height=625)
config = {'font': ('Arial', '14')}

rules_form = RulesView(
    model=expert_sys_model,
    controller=expert_sys_controller,
    master=root,
    **config)

states_form = StatesView(
    model=expert_sys_model,
    controller=expert_sys_controller,
    master=root,
    **config)

root.mainloop()