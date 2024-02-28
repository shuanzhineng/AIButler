INIT_MENU = [
    {
        "name": "系统管理",
        "icon": "xxx",
        "sort": 10000,
        "is_link": False,
        "link_url": "",
        "genre": "DIRECTORY",
        "web_path": "",
        "disabled": False,
        "apis": [],
        "children": [
            {
                "name": "菜单管理",
                "icon": "xxx",
                "sort": 11000,
                "is_link": False,
                "link_url": "",
                "genre": "PAGE",
                "web_path": "/menus",
                "disabled": False,
                "apis": [],
                "children": [
                    {
                        "name": "查询",
                        "sort": 11100,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "GET",
                                "api": "/system/menus"
                            }
                        ],
                    },
                    {
                        "name": "详情",
                        "sort": 11200,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "GET",
                                "api": "/system/menus/{id}"
                            }
                        ],
                    },
                    {
                        "name": "新增",
                        "sort": 11300,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "POST",
                                "api": "/system/menus"
                            }
                        ],
                    },
                    {
                        "name": "编辑",
                        "sort": 11400,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "PUT",
                                "api": "/system/menus/{id}"
                            },
                            {
                                "method": "PATCH",
                                "api": "/system/menus/{id}"
                            },
                        ],
                    },
                    {
                        "name": "删除",
                        "sort": 11500,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "DELETE",
                                "api": "/system/menus/{id}"
                            },
                        ],
                    },
                ]
            },
            {
                "name": "角色管理",
                "icon": "xxx",
                "sort": 12000,
                "is_link": False,
                "link_url": "",
                "genre": "PAGE",
                "web_path": "/roles",
                "disabled": False,
                "apis": [],
                "children": [
                    {
                        "name": "查询",
                        "sort": 12100,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "GET",
                                "api": "/system/roles"
                            }
                        ],
                    },
                    {
                        "name": "详情",
                        "sort": 12200,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "GET",
                                "api": "/system/roles/{id}"
                            }
                        ],
                    },
                    {
                        "name": "新增",
                        "sort": 12300,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "POST",
                                "api": "/system/roles"
                            }
                        ],
                    },
                    {
                        "name": "编辑",
                        "sort": 12400,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "PUT",
                                "api": "/system/roles/{id}"
                            },
                            {
                                "method": "PATCH",
                                "api": "/system/roles/{id}"
                            },
                        ],
                    },
                    {
                        "name": "删除",
                        "sort": 12500,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "DELETE",
                                "api": "/system/roles/{id}"
                            },
                        ],
                    },
                ]
            },
            {
                "name": "部门管理",
                "icon": "xxx",
                "sort": 13000,
                "is_link": False,
                "link_url": "",
                "genre": "PAGE",
                "web_path": "/depts",
                "disabled": False,
                "apis": [],
                "children": [
                    {
                        "name": "查询",
                        "sort": 13100,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "GET",
                                "api": "/system/depts"
                            }
                        ],
                    },
                    {
                        "name": "详情",
                        "sort": 13200,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "GET",
                                "api": "/system/depts/{id}"
                            }
                        ],
                    },
                    {
                        "name": "新增",
                        "sort": 13300,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "POST",
                                "api": "/system/depts"
                            }
                        ],
                    },
                    {
                        "name": "编辑",
                        "sort": 13400,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "PUT",
                                "api": "/system/depts/{id}"
                            },
                            {
                                "method": "PATCH",
                                "api": "/system/depts/{id}"
                            },
                        ],
                    },
                    {
                        "name": "删除",
                        "sort": 13500,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "DELETE",
                                "api": "/system/depts/{id}"
                            },
                        ],
                    },
                ]
            },
            {
                "name": "用户管理",
                "icon": "xxx",
                "sort": 14000,
                "is_link": False,
                "link_url": "",
                "genre": "PAGE",
                "web_path": "/users",
                "disabled": False,
                "children": [
                    {
                        "name": "查询",
                        "sort": 13100,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "GET",
                                "api": "/system/users"
                            }
                        ],
                    },
                    {
                        "name": "详情",
                        "sort": 13200,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "GET",
                                "api": "/system/users/{id}"
                            }
                        ],
                    },
                    {
                        "name": "新增",
                        "sort": 13300,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "POST",
                                "api": "/system/users"
                            }
                        ],
                    },
                    {
                        "name": "编辑",
                        "sort": 13400,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "PUT",
                                "api": "/system/users/{id}"
                            },
                            {
                                "method": "PATCH",
                                "api": "/system/users/{id}"
                            },
                        ],
                    },
                    {
                        "name": "删除",
                        "sort": 13500,
                        "genre": "BUTTON",
                        "disabled": False,
                        "apis": [
                            {
                                "method": "DELETE",
                                "api": "/system/users/{id}"
                            },
                        ],
                    },
                ]
            }
        ]
    }

]