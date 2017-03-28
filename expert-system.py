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


class ExpertSysView(Frame):
    ''' Интерфейс к программе '''
    def __init__(self, model=None, controller=None, master=None, **config):
        self.model = model
        self.controller = controller
        self.controller.set_view(self)
        super().__init__(master)
        self.configure(bg='black')
        self.pack(expand='yes', fill='both', padx=5, pady=5)
        self.create_widgets(**config)

    def create_widgets(self, **config):
        # delete
        frame_delete = Frame(self)
        self.delete_but = Button(frame_delete,
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
                          text='Загрузить правила',
                          bg='#bebeee',
                          command=self.load_rules,
                          **config)
        save_but = Button(frame_loadsave,
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


expert_sys_model = ExpertSysModel()
expert_sys_controller = ExpertSysController(expert_sys_model)

root = Tk()
root.title('Expert System')
root.geometry('470x640+100+100')
root.minsize(width=470, height=640)
config = {'font': ('Arial', '14')}

expert_sys_interface = ExpertSysView(
    model=expert_sys_model,
    controller=expert_sys_controller,
    master=root,
    **config)

expert_sys_interface.mainloop()