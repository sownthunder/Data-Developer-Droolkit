"""
            # Name Input
            ttk.Label(master=self.lblframe_create, text='Name: ').grid(row=0, column=0, padx=5,
                                                                       pady=5, sticky='w')
            self.name = ttk.Entry(master=self.lblframe_create, width=24)  # [2019-11-18]\\ borderwidth=3)
            self.name.grid(row=0, column=1, sticky='w', padx=5, pady=5)

            # xXxXxXxXxXxXxXxXx
            # Email Input
            ttk.Label(master=self.lblframe_create, text='Email: ').grid(row=1, column=0, padx=5,
                                                                        pady=5, sticky='w')
            self.email = ttk.Entry(master=self.lblframe_create, width=24)  # [2019-11-18]\\ borderwidth=3)
            self.email.grid(row=1, column=1, sticky='w', padx=5, pady=5)

            # xXxXxXxXxXxXxXxXx
            # Type Input
            ttk.Label(master=self.lblframe_create, text='Type: ').grid(row=2, column=0, padx=5,
                                                                       pady=5, sticky='w')
            ############################
            # RADIO-VARIABLE == STRING #
            self.radio_type_var = tk.StringVar(master=self.lblframe_create, value="email")
            ################################################################################
            self.radio_type_1 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_type_var,
                                                value="web", text="Web", width=15)  # style="TButton")
            self.radio_type_1.grid(row=2, column=1, columnspan=2, sticky='w', padx=5, pady=5)
            self.radio_type_2 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_type_var,
                                                value="email", text="Email", width=15)
            self.radio_type_2.grid(row=2, column=1, columnspan=2, sticky='e', padx=55, pady=5)

            # xXxXxXxXxXxXxXxXx
            # Sent Input
            ttk.Label(master=self.lblframe_create, text='Sent: ').grid(row=3, column=0, padx=5,
                                                                       pady=5, stick='w')
            ##########################
            # RADIO-VARIABLE == BOOL #
            self.radio_sent_var = tk.BooleanVar(master=self.lblframe_create, value=False)
            ################################################################################
            self.radio_sent_1 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_sent_var,
                                                value=True, text="Yes", width=15, state=tk.DISABLED)  # style="TButton")
            self.radio_sent_1.grid(row=3, column=1, sticky='w', padx=5, pady=5)
            self.radio_sent_2 = ttk.Radiobutton(master=self.lblframe_create, variable=self.radio_sent_var,
                                                value=False, text="No", width=15)
            self.radio_sent_2.grid(row=3, column=1, sticky='e', padx=5, pady=5)

            # TRACKING NUMBER #
            ttk.Label(master=self.lblframe_create, text='Tracking #: ').grid(row=5, column=0,
                                                                             padx=5, pady=5, sticky='w')
            self.tracking_num = ttk.Entry(master=self.lblframe_create, width=24, state='readonly')
            self.tracking_num.grid(row=5, column=1, sticky='w', padx=5, pady=5)

            # Timestamp (start_time)
            self.start_time_var = tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text="Timestamp: ").grid(row=6, column=0, padx=5, pady=5, sticky='w')

            # <<< CLOCK (timestamp_test) >>>
            self.clock = ttk.Label(master=self.lblframe_create, font=("Calibri", 20, 'bold'),
                                   background='#2b303b', foreground="#bbc0c9")
            self.clock.grid(row=6, column=1, padx=5, pady=5, stick='w')

            # Initials (agilent worker)
            self.initials_var = tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text='Initials: ', font=("Calibri", 12, 'bold'),
                      background='#666666', foreground='#000000').grid(row=7, column=0, sticky='w', padx=5, pady=5)
            self.initials = ttk.Entry(master=self.lblframe_create, width=24)
            self.initials.grid(row=7, column=1, sticky='w', padx=5, pady=5)

            # account_id [row=8]
            self.account_id_var = tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text="Account ID: ").grid(row=8, column=0, sticky='w', padx=5,
                                                                             pady=5)
            self.account_id = ttk.Entry(master=self.lblframe_create, width=24)
            self.account_id.grid(row=8, column=1, sticky='w', padx=5, pady=5)
            
            # PRODUCT_NUMBER [row=9]
            self.product_num_var = tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text='Product #: ').grid(row=9, column=0, sticky='w', padx=5,
                                                                            pady=5)
            self.product_num = ttk.Entry(master=self.lblframe_create, width=24)
            self.product_num.grid(row=9, column=1, sticky='w', padx=5, pady=5)

            # prodflow quote number [row=10]
            self.prodflow_quote_var = tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text='Prodflow Quote #: ').grid(row=10, column=0, sticky='w', padx=5,
                                                                                   pady=5)
            self.prodflow_quote_num = ttk.Entry(master=self.lblframe_create, width=24)
            self.prodflow_quote_num.grid(row=10, column=1, sticky='w', padx=5, pady=5)

            # SAP quote number [row=11]
            self.sap_quote_var = tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text='SAP Quote #: ').grid(row=11, column=0, sticky='w', padx=5,
                                                                              pady=5)
            self.sap_quote_num = ttk.Entry(master=self.lblframe_create, 
                                           textvariable=self.sap_quote_var,
                                           width=24)
            self.sap_quote_num.grid(row=11, column=1, sticky='w', padx=5, pady=5)
            
            # company name [row=12]
            self.company_var= tk.StringVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text='Company Name: ').grid(row=12, column=0, sticky='w', padx=5, pady=5)
            self.company_name = ttk.Entry(master=self.lblframe_create, 
                                          textvariable=self.company_var, 
                                          width=24)
            self.company_name.grid(row=12, column=1, sticky='w', padx=5, pady=5)

            # price [row=11]
            """ [2019-12-31] """
            """
            self.price_var = tk.IntVar(master=self.lblframe_create)
            ttk.Label(master=self.lblframe_create, text='Price: ').grid(row=11, column=0, sticky='w', padx=5, pady=5)
            self.price = ttk.Entry(master=self.lblframe_create, width=24)
            self.price.grid(row=11, column=1, sticky='w', padx=5, pady=5)
            """

            # notes [row=13/14]
            # xXxXxXxXxXxXxXxXx
            # Notes Section
            ttk.Label(master=self.lblframe_create, text="NOTES: ").grid(row=13, column=0,
                                                                        padx=5, pady=5, sticky='w')
            self.notes_var = tk.StringVar(master=self.lblframe_create)
            self.notes = tk.Entry(master=self.lblframe_create, 
                                  textvariable=self.notes_var, 
                                  width=24)
            # [2019-12-30]\\self.notes = ttk.Entry(master=self.lblframe_create, width=24)
            self.notes.grid(row=13, column=1, columnspan=2, rowspan=2, padx=5, pady=5, sticky='w')

            """[2019-12-12]"""
            """
            self.notes = ttk.Notebook(master=self.lblframe_create, height=200, width=200, padding=(1, 1))
            # Create the pages
            self.note_tab = tk.Text(master=self.lblframe_create, height=15, width=15,
                                    background="#96A853")  # ttk.Frame(master = self.notes)
            self.trackingnum_tab = tk.Text(master=self.lblframe_create, height=15, width=15,
                                           background="#2D323C")
            self.quotenum_tab = tk.Text(master=self.lblframe_create, height=15, width=15,
                                        background="#96A853")
            self.timestamp_tab = tk.Text(master=self.lblframe_create, height=15, width=15)
            # Add them to the notebook
            self.notes.add(self.note_tab, text="NOTES", )
            self.notes.add(self.trackingnum_tab, text="NOTES 2")
            self.notes.add(self.quotenum_tab, text="NOTES 3")
            self.notes.add(self.timestamp_tab, text="NOTES 4")
            """

            # keep_em_seperated = ttk.Separator(master=self.lblframe_create, orient=tk.HORIZONTAL)
            # keep_em_seperated.grid(row=6, column=0, columnspan=4)

            # [2019-11-20]\\self.notes.grid(row=5, column=0, columnspan=2, padx=5, sticky='n')
            # [2019-12-29]\\self.notes.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='n')
            # row = 6, column = 0, columnspan = 2 AND NO STICK OR PADX
            """