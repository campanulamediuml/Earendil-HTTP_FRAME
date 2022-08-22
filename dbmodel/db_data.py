from anduin import Data


class table():
    TABLE_USER = 'user'

    @staticmethod
    def create_init_db():
        Data.query('drop table %s'%table.TABLE_USER)
        column = [
            ('id', 'int', 'AUTO_INCREMENT', 'primary key'),
            ('username', 'varchar(1024)', 'default ""','comment "用户名"'),
            # 用户名
            ('pw_hash', 'varchar(1024)', 'default ""','comment "密码哈希"'),
            # 密码哈希
            ('comment', 'varchar(1024)', 'default ""','comment "备注"'),
            # 备注
            ('c_time', 'int', 'default 0','comment "创建时间"'),
            # 创建时间
            ('u_time', 'int', 'default 0','comment "更新时间"'),
            # 更新时间
            ('status', 'int', 'default 0','comment "账号状态"'),
            # 状态
        ]
        Data.create(table.TABLE_USER,column)


