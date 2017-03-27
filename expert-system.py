from tkinter import *
from collections import OrderedDict


class ExpertSysModel:  # Хранение данных и операциии по обработке данных
    def __init__(self):
        self.rules = OrderedDict()

    def add_rule(self, new_rule):
        pass


class ExpertSysController:  # Управления функциями модели. Данные методы вызываются из Вида
    def __init__(self, model=None):
        self.model = model


class FormRule(Frame):
    def __init__(self, model=None, controller=None, master=None, **config):
        self.model = model
        self.controller = controller
        super().__init__(master)
        self.configure(bg='black')
        self.pack(expand='yes', fill='both', padx=5, pady=5)
        self.create_widgets(**config)
        self.line_num = 0

    def create_widgets(self, **config):
        # delete
        frame_delete = Frame(self)
        delete_but = Button(frame_delete,
                            text='Удалить',
                            bg='#eebebe',
                            command=self.delete_rule,
                            **config)
        self.delete_rule_num_ver = StringVar()
        spinbox = Spinbox(frame_delete,
                          width=5,
                          from_=1, to=10,
                          textvariable=self.delete_rule_num_ver,
                          **config)
        # delete packed
        frame_delete.pack(side='top', fill='x')
        Label(frame_delete, text='Номер правила на удаление:', **config).pack(side='left')
        delete_but.pack(side='right', padx=5, pady=5)
        spinbox.pack(side='right', fill='y', pady=5)

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
                               command=self.add_rule,
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

    def save_rules(self):
        print('save rules')

    def load_rules(self):
        print('load rules')

    def delete_rule(self):
        print('delete rule')

    def add_rule(self):
        ''' добавление правила в список '''
        cond = self.conditions_var.get()
        res = self.result_var.get()
        prob = int(self.probability_var.get())
        if cond and res and prob:
            if cond not in self.model.rules:
                self.line_num += 1
                self.model.rules[cond] = (res, prob)
                line = '{0}. ЕСЛИ {1} ТО {2} ({3}%)\n'.format(self.line_num,
                                                              cond, res, prob)
                print(self.model.rules, self.line_num)
                self.rules_txt['state'] = 'normal'
                self.rules_txt.insert('{0}.{1}'.format(self.line_num, 0), line)
                self.rules_txt['state'] = 'disabled'
                self.rules_txt.see('{0}.{1}'.format(self.line_num, 0))


expert_sys_model = ExpertSysModel()
expert_sys_controller = ExpertSysController(expert_sys_model)

root = Tk()
root.title('Expert System')
root.geometry('470x640+100+100')
root.minsize(width=470, height=640)
config = {'font': ('Arial', '14')}

expert_sys_interface = FormRule(
    model=expert_sys_model,
    controller=expert_sys_controller,
    master=root,
    **config)

expert_sys_interface.mainloop()