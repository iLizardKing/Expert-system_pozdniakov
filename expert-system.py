from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from collections import OrderedDict
import re


class ExpertSysModel:
    ''' Хранение данных и операций по обработке данных '''
    def __init__(self):
        self.rules = OrderedDict()

    def add_rule(self, condition, result, probability):
        self.rules[condition] = (result, probability)

    def get_rules_amount(self):
        return len(self.rules)


class ExpertSysController:
    ''' Управления функциями МОДЕЛИ. Данные методы вызываются из ВИДА '''
    def __init__(self, model=None):
        self.model = model

    def set_view(self, view):
        self.view = view

    def add_new_rule(self):
        ''' добавление нового правила в МОДЕЛЬ '''
        condition = self.view.conditions_var.get()
        result = self.view.result_var.get()
        probability = int(self.view.probability_var.get())
        if condition and result:
            if condition not in self.model.rules:
                self.model.add_rule(condition, result, probability)
                self.view.conditions_var.set('')
                self.view.result_var.set('')
                self.view.probability_var.set(100)
                self.view.refresh_rules()
            else:
                self.view.ok_message('Правило "{}" уже есть в системе'.format(condition))

    def delete_rule(self):
        num = self.view.delete_rule_num.get()
        if num:
            num = int(num) - 1
            condition = list(self.model.rules)[num]
            del self.model.rules[condition]
            self.view.refresh_rules()

    def add_condition(self):
        print('add_condition')

    def delete_condition(self):
        print('delete_condition')

    rule_re = re.compile(r'\d{1,2}\. ЕСЛИ (?P<cond>\w+) ТО (?P<res>\w+) \((?P<prob>\d{1,3})%\)')

    def load_rules_from_file(self, file):
        self.model.rules = OrderedDict()
        for line in file:
            match = __class__.rule_re.match(line)
            if match:
                condition = match.group('cond')
                result = match.group('res')
                probability = int(match.group('prob'))
                self.model.add_rule(condition, result, probability)
            else:
                print('Ошибка! Очередная строка не соответствует шаблону.\n"{}"'.format(line))
        file.close()
        self.view.refresh_rules()

    def save_rules_to_file(self, file):
        for num, rule in enumerate(self.model.rules.items()):
            condition, result, probability = rule[0], rule[1][0], rule[1][1]
            line = '{0}. ЕСЛИ {1} ТО {2} ({3}%)'.format(num+1, condition, result, probability)
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
        self.controller.set_view(self)
        super().__init__(master)
        self.configure(bg='black')
        self.pack(side='left', expand='yes', fill='both', padx=5, pady=5)
        self.create_widgets(**config)

    def create_widgets(self, **config):
        # delete
        frame_delete = Frame(self)
        self.delete_but = Button(frame_delete,
                                 bd=3,
                                 text='Удалить',
                                 bg='#eebebe',
                                 command=self.controller.delete_rule,
                                 state='disabled',
                                 **config)
        self.delete_rule_num = StringVar(0)
        self.spinbox = Spinbox(frame_delete,
                               width=5,
                               from_=0, to=0,
                               textvariable=self.delete_rule_num,
                               state='disabled',
                               **config)
        # delete packed
        frame_delete.pack(side='top', fill='x')
        Label(frame_delete, text='Номер правила на удаление:', **config).pack(side='left')
        self.delete_but.pack(side='right', padx=5, pady=5)
        self.spinbox.pack(side='right', fill='y', pady=5)

        # text
        frame_text = Frame(self)
        self.rules_txt = Text(frame_text,
                              width=40,
                              height=15,
                              state='disabled',
                              wrap='word',
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
        self.probability_var = IntVar(value=100)
        probability_scl = Scale(frame_add_child,
                                variable=self.probability_var,
                                orient=HORIZONTAL,
                                from_=0, to=100,
                                tickinterval=10,
                                resolution=1)
        add_rules_but = Button(frame_add_parent,
                               bd=3,
                               text="Добавить",
                               bg='#bed6be',
                               command=self.controller.add_new_rule,
                               **config)
        # add packed
        frame_add_parent.pack(side='top', fill='x')
        frame_add_child.pack(side='left', expand=True, fill='x')
        Label(frame_add_child, text="Условия:", **config).pack(anchor=W)
        conditions_ent.pack(fill='x')
        Label(frame_add_child, text="Результат:", **config).pack(anchor=W)
        result_ent.pack(fill='x')
        Label(frame_add_child, text="Вероятность:", **config).pack(anchor=W)
        probability_scl.pack(fill='x')
        add_rules_but.pack(side='right', fill='both', pady=5)

        # load|safe
        frame_loadsave = Frame(self)
        load_but = Button(frame_loadsave,
                          bd=3,
                          text='Загрузить правила',
                          bg='#bebeee',
                          command=self.load_rules,
                          **config)
        save_but = Button(frame_loadsave,
                          bd=3,
                          text='Сохранить правила',
                          bg='#bebeee',
                          command=self.save_rules,
                          **config)
        # load|safe packed
        frame_loadsave.pack(side='top', fill='x')
        load_but.pack(side='left', expand=True, fill='x')
        save_but.pack(side='right', expand=True, fill='x')

    def ok_message(self, message):
        messagebox.showinfo('Ошибка', message)

    def refresh_rules(self):
        ''' Обновляет список правил в соответствии с моделью '''
        rules_amount = self.model.get_rules_amount()
        if rules_amount > 0:
            self.spinbox.config(state='normal', from_=1, to=rules_amount)
            self.delete_but.config(state='normal')
            self.delete_rule_num.set(1)
            self.rules_txt.config(state='normal')
            self.rules_txt.delete('1.0', END)
            for num, rule in enumerate(self.model.rules.items()):
                condition, result, probability = rule[0], rule[1][0], rule[1][1]
                template = '{0}. ЕСЛИ {1} ТО {2} ({3}%)\n'
                line = template.format(num+1,
                                       condition,
                                       result,
                                       probability)
                self.rules_txt.insert('{0}.{1}'.format(num+1, 0), line)
            self.rules_txt.config(state='disabled')
            self.rules_txt.see('{0}.{1}'.format(num+1, 0))
        else:
            self.delete_rule_num.set(0)
            self.spinbox.config(from_=0, to=0, state='disabled')
            self.delete_but.config(state='disabled')
            self.rules_txt.config(state='normal')
            self.rules_txt.delete('1.0', END)
            self.rules_txt.config(state='disabled')

    def save_rules(self):
        file_var = filedialog.asksaveasfile(mode='w', defaultextension=".rules")
        self.controller.save_rules_to_file(file_var)

    def load_rules(self):
        filename = filedialog.askopenfilename(filetypes=[('*.rules files', '*.rules')])
        file_var = open(filename, 'r')
        self.controller.load_rules_from_file(file_var)


class ConditionView(Frame):
    def __init__(self, model=None, controller=None, master=None, **config):
        self.model = model
        self.controller = controller
        self.controller.set_view(self)
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
                                    command=self.controller.add_condition,
                                    **config)
        # PACKED add conditions with entry, scroll & button
        frame_add_parent.pack(side='top', fill='x')
        frame_add_child.pack(side='left', expand=True, fill='x')
        Label(frame_add_child, text="Состояние:", **config).pack(anchor=W)
        conditions_ent.pack(fill='x')
        Label(frame_add_child, text="Степень:", **config).pack(anchor=W)
        probability_scl.pack(fill='x')
        conditions_add_but.pack(side='right', fill='both', pady=5)

        # conditions text with opportunity to delete (spinbox & button),
        # save & load buttons
        frame_text_parent = Frame(self)
        frame_text_child = Frame(frame_text_parent)
        self.conditions_txt = Text(frame_text_child,
                                   width=20,
                                   height=10,
                                   state='disabled',
                                   wrap='word',
                                   **config)
        conditions_scrollbar = Scrollbar(frame_text_child,
                                         command=self.conditions_txt.yview)
        self.conditions_txt.config(yscrollcommand=conditions_scrollbar.set)
        self.delete_rule_num = StringVar(0)
        self.delete_spinbox = Spinbox(frame_text_parent,
                                      width=5,
                                      from_=0, to=0,
                                      textvariable=self.delete_rule_num,
                                      state='disabled',
                                      **config)
        self.conditions_delete_but = Button(frame_text_parent,
                                            width=9,
                                            text='Удалить',
                                            bg='#eebebe',
                                            state='disabled',
                                            command=self.controller.delete_condition,
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
        frame_text_parent.pack(side='top', fill='both')
        frame_text_child.pack(side='left', expand=True, fill='x')
        self.conditions_txt.pack(side='left', expand=True, fill='both', pady=5)
        conditions_scrollbar.pack(side='left', fill='y', pady=5)
        self.delete_spinbox.pack(side='top',fill='x', pady=5)
        self.conditions_delete_but.pack(side='top', fill='x', pady=5)
        save_conditions_but.pack(side='top', fill='x', expand=True, anchor='s')
        load_conditions_but.pack(side='bottom', fill='x', pady=5)

        # result text, start button, save result button
        frame_result_parent = Frame(self, bg='#ffffd0')
        frame_result_child_txt = Frame(frame_result_parent)
        frame_result_child_btn = Frame(frame_result_parent)
        self.result_txt = Text(frame_result_child_txt,
                               width=30,
                               height=10,
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
        frame_result_child_txt.pack(side='top', fill='both', expand=True)
        self.result_txt.pack(side='left', expand=True, fill='both')
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
root.title('Expert System')
root.config(bg='grey')
root.geometry('900x640+100+100')
root.minsize(width=470, height=640)
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