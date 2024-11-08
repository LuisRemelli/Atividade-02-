from psycopg2.extras import RealDictCursor
import hashlib
from database.connectionDb import ConnectionDb
class UserORM:

    @staticmethod
    def authenticate_user(username: str, password: str):
        # Convertendo a senha para MD5
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        conn = ConnectionDb.get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = "select * from public.usuario u where u.email = %s and u.senha = %s"
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    
    @staticmethod
    def get_menus(user_id: int):
        conn = ConnectionDb.get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("select * from estrutura.menu where menu_id IS NULL AND id in (select menu_id from estrutura.perfil_menu pm where perfil_permissao_id in (select estrutura_perfil_permissao_id from public.usuario u where id = %s)) ORDER BY ordem", (str(user_id)))
        menus = cursor.fetchall()
        print("menus", menus)
        for menu in menus:
            menu_id = menu["id"]
            
            cursor.execute("select * from estrutura.menu where menu_id=%s AND id in (select menu_id from estrutura.perfil_menu pm where perfil_permissao_id in (select estrutura_perfil_permissao_id from public.usuario u where id = %s)) ORDER BY ordem", (str(menu_id), str(user_id)))
            # cursor.execute("SELECT id, ordem, titulo, icone, link FROM menus WHERE parent_id = %s ORDER BY ordem", (menu["id"],))
            menu["submenus"] = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return menus

    @staticmethod
    def get_telas(user_id: int):
        conn = ConnectionDb.get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        telas = []
        
        cursor.execute("select * from estrutura.perfil_tela where perfil_permissao_id in (select estrutura_perfil_permissao_id from public.usuario u where id = %s)", (str(user_id),))
        perfil_telas = cursor.fetchall()
        for perfil_tela in perfil_telas:
            perfil_tela_id = perfil_tela["id"]
            tela_id=perfil_tela["tela_id"]
            cursor.execute("select id, titulo, hint from estrutura.tela where id=%s", (tela_id))
            tela = cursor.fetchone()
            
            cursor.execute("select tipo_acao from estrutura.acao where perfil_tela_id = %s", (perfil_tela_id))
            telas["acoes"] = cursor.fetchall()
            
            telas.append(tela)
        
        
        
        cursor.close()
        conn.close()
        return telas