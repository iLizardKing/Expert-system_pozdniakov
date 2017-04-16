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
        self.conditions = list()
        self.result = list()

    def add_rule(self, name, condition, result):
        self.rules.append(
            Rule(name, condition, result)
        )

    def edit_rule(self, num, name, condition, result):
        self.rules[num] = Rule(name, condition, result)

    def get_rules_amount(self):
        return len(self.rules)

    def add_condition(self, condition, probability):
        self.conditions.append((condition, probability))

    def get_conditions_amount(self):
        return len(self.conditions)


class ExpertSysController:
    ''' Управления функциями МОДЕЛИ. Данные методы вызываются из ВИДА '''
    def __init__(self, model=None):
        self.model = model
        self.rule_view = None
        self.cond_view = None
        self.edit_mode = False
        self.edit_num = None

    def set_view(self, rule_view=None, cond_view=None):
        if rule_view:
            self.rule_view = rule_view
        if cond_view:
            self.cond_view = cond_view

    def add_new_rule(self):
        ''' добавление нового правила в МОДЕЛЬ '''
        name = self.rule_view.name_var.get()
        condition = self.rule_view.conditions_var.get()
        result = self.rule_view.result_var.get()
        if name and condition and result:
            if self.edit_mode:
                self.model.edit_rule(self.edit_num-1, name, condition, result)
                self.edit_mode = False
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
                self.rule_view.ok_message('Правило "{}" уже есть в системе'.format(name))

    def del_rule(self):
        num = int(self.rule_view.select_rule_num.get())
        if num:
            del self.model.rules[num-1]
            self.rule_view.refresh_rules()

    def edit_rule(self):
        num = int(self.rule_view.select_rule_num.get())
        if num:
            self.edit_mode = True
            self.edit_num = num
            cond = self.model.rules[num-1].condition
            name = self.model.rules[num-1].name
            res = self.model.rules[num-1].result
            self.rule_view.name_var.set(name)
            self.rule_view.conditions_var.set(cond)
            self.rule_view.result_var.set(res)
            self.rule_view.refresh_rules()

    def add_new_condition(self):
        ''' добавление нового состояния в МОДЕЛЬ '''
        condition = self.cond_view.conditions_var.get()
        probability = int(self.cond_view.probability_var.get())
        if condition:
            self.model.conditions.append((condition, probability))

        print(self.model.conditions)

    def del_condition(self):
        print('delete_condition')

    rule_re = re.compile(r'\d{1,2}\) ПРАВИЛО (?P<name>\w+) ЕСЛИ (?P<cond>\w+) ТО (?P<res>\w+)\.')

    def load_rules_from_file(self, file):
        self.model.rules = []
        for line in file:
            match = __class__.rule_re.match(line)
            if match:
                name = match.group('name')
                condition = match.group('cond')
                result = match.group('res')
                self.model.add_rule(name, condition, result)
            else:
                print('Ошибка! Очередная строка не соответствует шаблону.\n"{}"'.format(line))
        file.close()
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

    def load_conditions_from_file(self, file):
        print('controller - load_conditions_from_file')

    def save_conditions_to_file(self, file):
        print('controller - save_conditions_to_file')

    def save_result_to_file(self, file):
        print('controller - save_result_to_file')

    def start_processing(self):
        print('controller - start processing')


class RulesView(Frame):
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
                                 bg='#bed6be',
                                 command=self.controller.edit_rule,
                                 state='disabled',
                                 **config)
        self.select_rule_num = StringVar(0)
        self.spinbox = Spinbox(frame_delete,
                               width=5,
                               from_=0, to=0,
                               textvariable=self.select_rule_num,
                               state='disabled',
                               **config)
        # delete|edit packed
        frame_delete.pack(side='top', fill='x')
        Label(frame_delete, text='Номер правила:', **config).pack(side='left')
        self.delete_but.pack(side='right', padx=5, pady=5)
        self.edit_but.pack(side='right', padx=5, pady=5)
        self.spinbox.pack(side='right', fill='y', pady=5)

        # text
        frame_text = Frame(self)
        self.rules_txt = Text(frame_text,
                              width=40,
                              height=15,
                              wrap='word',
                              state='disabled',
                              **config)
        scrollbar = Scrollbar(frame_text,
                              command=self.rules_txt.yview)
        self.rules_txt.config(yscrollcommand=scrollbar.set)
        # text packed
        frame_text.pack(side='top', expand=True, fill='both')
        self.rules_txt.pack(side='left', expand=True, fill='both')
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
        frame_add_child.pack(side='left', expand=True, fill='x')
        Label(frame_add_child, text="Наименование:", **config).pack(anchor=W)
        name_ent.pack(fill='x')
        Label(frame_add_child, text="Условия:", **config).pack(anchor=W)
        conditions_ent.pack(fill='x')
        Label(frame_add_child, text="Результат:", **config).pack(anchor=W)
        result_ent.pack(fill='x')
        self.add_rules_but.pack(side='right', fill='both', pady=5)

        # load|safe
        frame_loadsave = Frame(self)
        load_but = Button(frame_loadsave,
                          bd=3,
                          text='Загрузить правила',
                          bg='#bebeee',
                          command=self.load_rules,
                          **config)
        self.save_but = Button(frame_loadsave,
                          bd=3,
                          text='Сохранить правила',
                          bg='#bebeee',
                          state='disabled',
                          command=self.save_rules,
                          **config)
        # load|safe packed
        frame_loadsave.pack(side='top', fill='x')
        load_but.pack(side='left', expand=True, fill='x')
        self.save_but.pack(side='right', expand=True, fill='x')

    def ok_message(self, message):
        messagebox.showinfo('Ошибка', message)

    def refresh_rules(self):
        ''' Обновляет список правил в соответствии с моделью '''
        rules_amount = self.model.get_rules_amount()
        if rules_amount > 0:
            if self.controller.edit_mode:
                self.add_rules_but.config(text='Редиктировать')
            else:
                self.add_rules_but.config(text='Добавить')
            self.spinbox.config(state='normal', from_=1, to=rules_amount)
            self.delete_but.config(state='normal')
            self.select_rule_num.set(1)
            self.edit_but.config(state='normal')
            self.save_but.config(state='normal')
            self.rules_txt.config(state='normal')
            self.rules_txt.delete('1.0', END)

            for num, rule in enumerate(self.model.rules):
                template = '{num}) ПРАВИЛО {name}\nЕСЛИ {condition}\nТО {result}\n\n'
                line = template.format(num=num+1,
                                       name=rule.name,
                                       condition=rule.condition,
                                       result=rule.result)
                self.rules_txt.insert('{0}.{1}'.format(num*4+1, 0), line)
            self.rules_txt.config(state='disabled')
            self.rules_txt.see('{0}.{1}'.format(num+1, 0))
        else:
            self.select_rule_num.set(0)
            self.spinbox.config(from_=0, to=0, state='disabled')
            self.delete_but.config(state='disabled')
            self.edit_but.config(state='disabled')
            self.save_but.config(state='disabled')
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


class ConditionView(Frame):
    def __init__(self, model=None, controller=None, master=None, **config):
        self.model = model
        self.controller = controller
        self.controller.set_view(cond_view=self)
        super().__init__(master)
        self.configure(bg='black')
        self.pack(side='left', expand='yes', fill='both', padx=5, pady=5)
        self.create_widgets(**config)

    def create_widgets(self, **config):
        # add conditions with entry, scroll & button
        frame_add_parent = Frame(self)
        frame_add_child = Frame(frame_add_parent)
        self.conditions_var = StringVar()
        conditions_ent = Entry(frame_add_child,
                               textvariable=self.conditions_var,
                               fg='grey',
                               **config)
        self.probability_var = IntVar(value=100)
        probability_scl = Scale(frame_add_child,
                                variable=self.probability_var,
                                orient=HORIZONTAL,
                                from_=0, to=100,
                                tickinterval=10,
                                resolution=1)
        conditions_add_but = Button(frame_add_parent,
                                    width=9, bd=3,
                                    text='Добавить',
                                    bg='#bed6be',
                                    command=self.controller.add_new_condition,
                                    **config)
        # PACKED add conditions with entry, scroll & button
        frame_add_parent.pack(side='top', fill='x')
        frame_add_child.pack(side='left', expand=True, fill='x')
        Label(frame_add_child, text="Состояние и степень:", **config).pack(anchor=W)
        conditions_ent.pack(fill='x')
        probability_scl.pack(fill='x')
        conditions_add_but.pack(side='right', fill='both', pady=5)

        # conditions text with opportunity to delete (spinbox & button),
        # save & load buttons
        frame_text_parent = Frame(self)
        frame_text_child = Frame(frame_text_parent)
        self.conditions_txt = Text(frame_text_child,
                                   width=25,
                                   height=12,
                                   wrap='word',
                                   state='disabled',
                                   **config)
        conditions_scrollbar = Scrollbar(frame_text_child,
                                         command=self.conditions_txt.yview)
        self.conditions_txt.config(yscrollcommand=conditions_scrollbar.set)
        self.del_conditions_num_var = StringVar(0)
        self.del_conditions_num_spin = Spinbox(frame_text_parent,
                                      width=5,
                                      from_=0, to=0,
                                      textvariable=self.del_conditions_num_var,
                                      state='disabled',
                                      **config)
        self.conditions_del_but = Button(frame_text_parent,
                                            width=9,
                                            text='Удалить',
                                            bg='#eebebe',
                                            state='disabled',
                                            command=self.controller.del_condition,
                                            **config)
        save_conditions_but = Button(frame_text_parent,
                                     width=9, bd=3,
                                     text='Сохранить\nсостояние',
                                     bg='#bebeee',
                                     command=self.save_conditions,
                                     **config)
        load_conditions_but = Button(frame_text_parent,
                                     width=9, bd=3,
                                     text='Загрузить\nсостояние',
                                     bg='#bebeee',
                                     command=self.load_conditions,
                                     **config)
        # PACKED conditions text with opportunity to delete (spinbox & button),
        # save & load buttons
        frame_text_parent.pack(side='top', expand=True, fill='both')
        frame_text_child.pack(side='left', expand=True, fill='both')
        self.conditions_txt.pack(side='left', expand=True, fill='both', pady=5)
        conditions_scrollbar.pack(side='left', fill='y', pady=5)
        self.del_conditions_num_spin.pack(side='top',fill='x', pady=5)
        self.conditions_del_but.pack(side='top', fill='x', pady=5)
        save_conditions_but.pack(side='top', fill='x', expand=True, anchor='s')
        load_conditions_but.pack(side='bottom', fill='x', pady=5)

        # result text, start button, save result button
        frame_result_parent = Frame(self, bg='#ffffd0')
        frame_result_child_txt = Frame(frame_result_parent)
        frame_result_child_btn = Frame(frame_result_parent)
        self.result_txt = Text(frame_result_child_txt,
                               width=35,
                               height=8,
                               state='disabled',
                               wrap='word',
                               **config)
        result_scrollbar = Scrollbar(frame_result_child_txt,
                              command=self.result_txt.yview)
        self.result_txt.config(yscrollcommand=result_scrollbar.set)
        start_but = Button(frame_result_child_btn,
                           bd=3,
                           text='Начать обработку',
                           command=self.controller.start_processing,
                           **config)
        save_result_but = Button(frame_result_child_btn,
                                 bd=3,
                                 text='Сохранить результат',
                                 bg='#bebeee',
                                 command=self.save_result,
                                 **config)
        # PACKED result text, start button, save result button
        frame_result_parent.pack(side='bottom', fill='x')
        frame_result_child_txt.pack(side='top', expand=True, fill='x')
        self.result_txt.pack(side='left', expand=True, fill='x')
        result_scrollbar.pack(side='left', fill='y')
        frame_result_child_btn.pack(side='bottom', fill='both')
        save_result_but.pack(side='left', expand=True, fill='x')
        start_but.pack(side='right', expand=True, fill='x')

    def load_conditions(self):
        print('view - load conditions')
        file = None
        self.controller.load_conditions_from_file(file)

    def save_conditions(self):
        print('view - save conditions')
        file = None
        self.controller.save_conditions_to_file(file)

    def save_result(self):
        print('view - save result')
        file = None
        self.controller.save_result_to_file(file)


expert_sys_model = ExpertSysModel()
expert_sys_controller = ExpertSysController(expert_sys_model)

root = Tk()
root.title('Экспертная система')
root.config(bg='grey')
root.geometry('889x632+100+100')
root.minsize(width=472, height=632)
config = {'font': ('Arial', '14')}

rules_form = RulesView(
    model=expert_sys_model,
    controller=expert_sys_controller,
    master=root,
    **config)

conditions_form = ConditionView(
    model=expert_sys_model,
    controller=expert_sys_controller,
    master=root,
    **config)

root.mainloop()