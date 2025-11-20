"""
SISTEMA PROFESSIONALNET - REDE SOCIAL PROFISSIONAL
Autor: Sistema de Gestão
Data: 2025
Descrição: Sistema completo de rede social profissional com validações, 
tratamento de exceções e estrutura de menu intuitiva.
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Generator
from pathlib import Path


class ProfessionalNet:
    """Classe principal do sistema ProfessionalNet - VERSÃO OTIMIZADA"""
    
    # Constantes de validação
    REGEX_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    MIN_USERNAME_LEN, MIN_SENHA_LEN, MAX_BIO_LEN = 3, 6, 200
    MAX_POST_LEN, MIN_POST_LEN, MAX_COMENTARIO = 500, 5, 200
    PAGINA_SIZE, ENCODING = 5, 'utf-8'
    
    # Dados de teste pré-configurados em formato de dicionário
    DADOS_PRECONFIGURADOS = {
        'nomes': {
            0: 'Ana Costa', 1: 'Bruno Martins', 2: 'Carlos Oliveira', 3: 'Diana Ferreira', 4: 'Eduardo Santos',
            5: 'Fernanda Lima', 6: 'Gustavo Pereira', 7: 'Helena Rocha', 8: 'Igor Mendes', 9: 'Juliana Gomes',
            10: 'Kevin Alves', 11: 'Larissa Dias', 12: 'Matheus Correia', 13: 'Natalia Souza', 14: 'Otavio Carvalho',
            15: 'Patricia Ribeiro', 16: 'Quentin Barbosa', 17: 'Rafaela Campos', 18: 'Samuel Costa', 19: 'Tania Monteiro',
            20: 'Ulisses Rodrigues', 21: 'Vanessa Duarte', 22: 'Wagner Nunes', 23: 'Ximena Lopez', 24: 'Yasmin Azevedo',
            25: 'Zoe Machado', 26: 'Adriana Teles', 27: 'Bernardo Silva', 28: 'Camila Rosa', 29: 'Daphne Oliveira',
            30: 'Emerson Costa', 31: 'Fabiana Souza', 32: 'Gilson Pereira', 33: 'Hercules Santos', 34: 'Iris Almeida',
            35: 'Jeferson Martins', 36: 'Katarina Dias', 37: 'Leonardo Campos', 38: 'Mariana Rocha', 39: 'Norberto Lima',
            40: 'Octavia Ferreira', 41: 'Pompeia Gomes', 42: 'Quasimodo Vargas', 43: 'Rosangela Pinto', 44: 'Sheila Castro',
            45: 'Tiago Morais', 46: 'Urania Neves', 47: 'Vicente Barbosa', 48: 'Wanda Ramos', 49: 'Xavier Fontes',
            50: 'Yara Mendes', 51: 'Zilda Moraes'
        },
        'titulos': {
            0: 'Desenvolvedor Python', 1: 'Designer UX/UI', 2: 'Engenheiro de Software', 3: 'Analista de Dados',
            4: 'Gerente de Projetos', 5: 'Especialista em Marketing', 6: 'Arquiteto de Sistemas', 7: 'DevOps Engineer',
            8: 'Data Scientist', 9: 'Front-end Developer', 10: 'Back-end Developer', 11: 'Full Stack Developer',
            12: 'DBA - Database Administrator', 13: 'Consultor de TI', 14: 'Gestor de Recursos Humanos',
            15: 'Especialista em Segurança', 16: 'Product Manager', 17: 'Scrum Master', 18: 'QA Engineer',
            19: 'Ilustrador Digital', 20: 'Redator Técnico', 21: 'Especialista em Cloud', 22: 'Mobile Developer'
        },
        'bios': {
            0: 'Apaixonado por tecnologia e inovação', 1: 'Sempre buscando novos desafios profissionais',
            2: 'Especialista em soluções criativas', 3: 'Amante de desenvolvimento sustentável',
            4: 'Focado em qualidade e excelência', 5: 'Colaborador e team player', 6: 'Entusiasta de programação',
            7: 'Criando o futuro através da tecnologia', 8: 'Dedicado ao aprendizado contínuo',
            9: 'Profissional versátil e adaptável', 10: 'Transformando ideias em realidade', 11: 'Conectando pessoas e soluções'
        }
    }
    
    def __init__(self):
        """Inicializa o sistema"""
        self.usuarios, self.conexoes, self.posts = {}, {}, []
        self.usuario_logado = None
        self._cache_posts = {}
        self.arquivo_usuarios = Path('dados_usuarios.json')
        self.arquivo_conexoes = Path('dados_conexoes.json')
        self.arquivo_posts = Path('dados_posts.json')
        self._carregar_dados()
    
    def _carregar_dados(self) -> None:
        """Carrega dados de JSON ou inicializa"""
        try:
            if self.arquivo_usuarios.exists():
                self.usuarios = self._ler_json(self.arquivo_usuarios)
                self.conexoes = self._ler_json(self.arquivo_conexoes)
                self.posts = self._ler_json(self.arquivo_posts)
                print("✅ Dados carregados com sucesso!")
            else:
                self._inicializar_dados_teste()
                self._salvar_dados()
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            self._inicializar_dados_teste()
    
    def _ler_json(self, arquivo: Path) -> Any:
        """Lê um arquivo JSON com tratamento eficiente"""
        with open(arquivo, 'r', encoding=self.ENCODING) as f:
            return json.load(f)
    
    def _salvar_dados(self) -> None:
        """Salva dados em JSON"""
        try:
            self._escrever_json(self.arquivo_usuarios, self.usuarios)
            self._escrever_json(self.arquivo_conexoes, self.conexoes)
            self._escrever_json(self.arquivo_posts, self.posts)
            self._cache_posts.clear()
        except Exception as e:
            print(f"❌ Erro ao salvar dados: {e}")
    
    def _escrever_json(self, arquivo: Path, dados: Any) -> None:
        """Escreve dados em JSON"""
        with open(arquivo, 'w', encoding=self.ENCODING) as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    
    def _inicializar_dados_teste(self) -> None:
        """Inicializa dados de teste"""
        try:
            agora = datetime.now().strftime('%d/%m/%Y %H:%M')
            self.usuarios = {
                'usuario1': self._criar_usuario('João Silva', 'joao@example.com', '123456', 
                                               'Desenvolvedor Python', 'Apaixonado por programação', agora),
                'usuario2': self._criar_usuario('Maria Santos', 'maria@example.com', '123456',
                                               'Designer UX/UI', 'Criando experiências incríveis', agora)
            }
            
            nomes_dict = self.DADOS_PRECONFIGURADOS['nomes']
            titulos_dict = self.DADOS_PRECONFIGURADOS['titulos']
            bios_dict = self.DADOS_PRECONFIGURADOS['bios']
            
            for i, nome in enumerate(nomes_dict.values(), 3):
                username = f'usuario{i}'
                self.usuarios[username] = self._criar_usuario(
                    nome, f'{nome.lower().replace(" ", ".")}@example.com', '123456',
                    titulos_dict[i % len(titulos_dict)], bios_dict[i % len(bios_dict)], agora
                )
            
            self.conexoes = {u: [] for u in self.usuarios}
            self.conexoes['usuario1'] = ['usuario2']
            self.conexoes['usuario2'] = ['usuario1']
            
            self.posts = [
                {'id': 1, 'usuario': 'usuario1', 'autor_nome': 'João Silva', 'conteudo': 'Bem-vindo ao ProfessionalNet! 🚀',
                 'data': agora, 'likes': [], 'comentarios': []},
                {'id': 2, 'usuario': 'usuario2', 'autor_nome': 'Maria Santos', 
                 'conteudo': 'Adorando este novo sistema! 💼', 'data': agora, 'likes': ['usuario1'], 'comentarios': []}
            ]
        except Exception as e:
            print(f"Erro ao inicializar dados: {e}")
    
    def _criar_usuario(self, nome: str, email: str, senha: str, titulo: str, bio: str, data: str) -> Dict:
        """Factory para criar usuário"""
        return {'nome': nome, 'email': email, 'senha': senha, 'titulo': titulo, 'bio': bio,
                'data_criacao': data, 'seguidores': [], 'seguindo': []}
    
    @staticmethod
    def _limpar_tela() -> None:
        """Limpa console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _validar_email(self, email: str) -> bool:
        """Valida email"""
        return bool(re.match(self.REGEX_EMAIL, email.strip()))
    
    def _validar_senha(self, senha: str) -> Tuple[bool, str]:
        """Valida senha"""
        if len(senha) < self.MIN_SENHA_LEN:
            return False, f"Mín. {self.MIN_SENHA_LEN} caracteres"
        if not any(c.isupper() for c in senha):
            return False, "Requer letra maiúscula"
        if not any(c.isdigit() for c in senha):
            return False, "Requer números"
        return True, "Válida"
    
    def _validar_username(self, username: str) -> Tuple[bool, str]:
        """Valida username"""
        username = username.strip()
        if len(username) < self.MIN_USERNAME_LEN:
            return False, f"Mín. {self.MIN_USERNAME_LEN} caracteres"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Apenas letras, números e _"
        return True, "Válido"
    
    def _buscar_usuarios(self, termo: str) -> Generator:
        """Generator para buscar usuários (otimizado)"""
        termo_lower = termo.lower()
        for username, dados in self.usuarios.items():
            if termo_lower in username or termo_lower in dados['nome'].lower():
                yield username, dados
    
    def _obter_posts_usuario(self, username: str) -> List[Dict]:
        """Obtém posts com cache"""
        if username not in self._cache_posts:
            self._cache_posts[username] = [p for p in self.posts if p['usuario'] == username]
        return self._cache_posts[username]
    
    def registrar_usuario(self) -> None:
        """Registra novo usuário"""
        self._limpar_tela()
        print("=" * 60)
        print("📝 REGISTRO DE NOVO USUÁRIO")
        print("=" * 60)
        
        try:
            # Username
            while True:
                username = input("\n👤 Username: ").strip()
                valido, msg = self._validar_username(username)
                if not valido or username in self.usuarios:
                    print(f"❌ {msg if not valido else 'Já existe'}")
                    continue
                break
            
            # Email
            while True:
                email = input("📧 Email: ").strip()
                if not self._validar_email(email) or any(u['email'] == email for u in self.usuarios.values()):
                    print("❌ Email inválido ou já existe")
                    continue
                break
            
            # Senha
            while True:
                senha = input("🔒 Senha: ").strip()
                valido, msg = self._validar_senha(senha)
                if not valido:
                    print(f"❌ {msg}")
                    continue
                if input("   Confirme: ").strip() != senha:
                    print("❌ Senhas não conferem")
                    continue
                break
            
            nome = input("✍️  Nome completo: ").strip()
            if not nome or len(nome) < 3:
                print("❌ Nome muito curto")
                return
            
            self.usuarios[username] = self._criar_usuario(
                nome, email, senha, input("💼 Título: ").strip() or "Profissional",
                input("📝 Bio (máx 200): ").strip()[:self.MAX_BIO_LEN] or "Sem bio",
                datetime.now().strftime('%d/%m/%Y %H:%M')
            )
            self.conexoes[username] = []
            self._salvar_dados()
            print(f"\n✅ Bem-vindo, {nome}!")
            input("\n👉 ENTER...")
        except KeyboardInterrupt:
            print("\n⚠️  Cancelado")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def fazer_login(self) -> bool:
        """Realiza login"""
        self._limpar_tela()
        print("=" * 60)
        print("🔐 LOGIN")
        print("=" * 60)
        
        try:
            username = input("\n👤 Username: ").strip()
            if username not in self.usuarios:
                print("❌ Usuário não encontrado")
                input("\n👉 ENTER...")
                return False
            
            if self.usuarios[username]['senha'] != input("🔒 Senha: ").strip():
                print("❌ Senha incorreta")
                input("\n👉 ENTER...")
                return False
            
            self.usuario_logado = username
            print(f"\n✅ Bem-vindo, {self.usuarios[username]['nome']}!")
            input("\n👉 ENTER...")
            return True
        except KeyboardInterrupt:
            print("\n⚠️  Cancelado")
            return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def visualizar_perfil_publico(self) -> None:
        """Menu de navegação pública"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print("👥 NAVEGAR POR PERFIS (SEM LOGIN)")
            print("=" * 60)
            print("\n1️⃣  - Buscar usuário")
            print("2️⃣  - Ver todos")
            print("3️⃣  - Voltar")
            
            opcao = input("\nOpção: ").strip()
            if opcao == '1':
                self._buscar_usuario_publico()
            elif opcao == '2':
                self._listar_todos_usuarios()
            elif opcao == '3':
                return
    
    def _buscar_usuario_publico(self) -> None:
        """Busca usuário"""
        self._limpar_tela()
        termo = input("=" * 60 + "\n🔍 BUSCAR\n" + "=" * 60 + "\nDigite nome/username: ").strip().lower()
        
        if not termo:
            print("⚠️  Vazio")
            input("\n👉 ENTER...")
            return
        
        resultados = list(self._buscar_usuarios(termo))
        if not resultados:
            print(f"❌ Nenhum usuário encontrado")
            input("\n👉 ENTER...")
            return
        
        self._exibir_resultados(resultados)
    
    def _exibir_resultados(self, resultados: List[Tuple]) -> None:
        """Exibe resultados e permite seleção"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print("👥 RESULTADOS")
            print("=" * 60)
            print(f"\n✅ {len(resultados)} encontrado(s):\n")
            
            for i, (username, dados) in enumerate(resultados, 1):
                print(f"{i}. {dados['nome']} (@{username})")
                print(f"   💼 {dados['titulo']}")
                print(f"   📝 {dados['bio'][:50]}...\n")
            
            print(f"{len(resultados) + 1}. Voltar")
            
            try:
                opcao = int(input("Escolha: ").strip())
                if opcao == len(resultados) + 1:
                    return
                if 1 <= opcao <= len(resultados):
                    self._exibir_perfil_publico(resultados[opcao - 1][0])
            except (ValueError, IndexError):
                print("❌ Inválido")
                input("\n👉 ENTER...")
    
    def _listar_todos_usuarios(self) -> None:
        """Lista usuários com paginação"""
        usuarios_lista = list(self.usuarios.items())
        total = (len(usuarios_lista) + self.PAGINA_SIZE - 1) // self.PAGINA_SIZE
        pagina = 0
        
        while True:
            self._limpar_tela()
            inicio = pagina * self.PAGINA_SIZE
            fim = min(inicio + self.PAGINA_SIZE, len(usuarios_lista))
            
            print("=" * 60)
            print("👥 TODOS OS USUÁRIOS")
            print("=" * 60)
            print(f"\n📄 Página {pagina + 1}/{total} (usuários {inicio + 1}-{fim})\n")
            
            for i, (username, dados) in enumerate(usuarios_lista[inicio:fim], inicio + 1):
                print(f"{i}. {dados['nome']} (@{username})")
                print(f"   💼 {dados['titulo']}\n")
            
            print("-" * 60)
            nav = []
            if pagina > 0:
                nav.append("A=Ant")
            if pagina < total - 1:
                nav.append("P=Prox")
            nav.extend(["N°=Ver", "V=Sair"])
            print(" | ".join(nav))
            
            opcao = input("\nOpção: ").strip().upper()
            
            if opcao == 'A' and pagina > 0:
                pagina -= 1
            elif opcao == 'P' and pagina < total - 1:
                pagina += 1
            elif opcao == 'V':
                return
            elif opcao.isdigit():
                num = int(opcao)
                if 1 <= num <= len(usuarios_lista):
                    self._exibir_perfil_publico(usuarios_lista[num - 1][0])
    
    def _exibir_perfil_publico(self, username: str) -> None:
        """Exibe perfil público"""
        while True:
            self._limpar_tela()
            
            if username not in self.usuarios:
                print("❌ Usuário não encontrado")
                return
            
            usuario = self.usuarios[username]
            posts = self._obter_posts_usuario(username)
            
            print("=" * 60)
            print("👤 PERFIL DO USUÁRIO")
            print("=" * 60)
            print(f"\n👤 {usuario['nome']} (@{username})")
            print(f"📧 {usuario['email']}")
            print(f"💼 {usuario['titulo']}")
            print(f"📝 {usuario['bio']}")
            print(f"📅 {usuario['data_criacao']}")
            print(f"\n🔗 Conexões: {len(self.conexoes.get(username, []))} | 👥 Seguidores: {len(usuario['seguidores'])} | 📌 Seguindo: {len(usuario['seguindo'])}")
            print(f"✍️  Posts: {len(posts)}")
            
            if not posts:
                print("\n⚠️  Sem posts")
                input("\n👉 ENTER...")
                return
            
            print("\n1️⃣  - Ver posts | 2️⃣  - Voltar")
            if input("\nOpção: ").strip() == '1':
                self._exibir_posts_usuario(username)
            else:
                return
    
    def _exibir_posts_usuario(self, username: str) -> None:
        """Exibe posts do usuário"""
        posts = self._obter_posts_usuario(username)
        if not posts:
            print("⚠️  Sem posts")
            input("\n👉 ENTER...")
            return
        
        usuario = self.usuarios[username]
        indice = 0
        
        while indice < len(posts):
            self._limpar_tela()
            post = posts[indice]
            
            print("=" * 60)
            print("📰 POSTS")
            print("=" * 60)
            print(f"\n👤 {usuario['nome']} (@{username})")
            print(f"💼 {usuario['titulo']}")
            print(f"\nPost {indice + 1}/{len(posts)}")
            print("-" * 60)
            print(f"📅 {post['data']}\n{post['conteudo']}\n")
            print("-" * 60)
            print(f"❤️  {len(post['likes'])} | 💬 {len(post['comentarios'])}")
            
            if post['comentarios']:
                print("\n💬:")
                for i, com in enumerate(post['comentarios'][:3], 1):
                    print(f"  {i}. {com['nome']}: {com['texto'][:40]}...")
                if len(post['comentarios']) > 3:
                    print(f"  +{len(post['comentarios']) - 3}")
            
            print("\n-" * 30)
            nav = []
            if indice > 0:
                nav.append("1=Ant")
            if indice < len(posts) - 1:
                nav.append("2=Prox")
            nav.append("3=Sair")
            print(" | ".join(nav))
            
            opcao = input("\nOpção: ").strip()
            if opcao == '1' and indice > 0:
                indice -= 1
            elif opcao == '2' and indice < len(posts) - 1:
                indice += 1
            elif opcao == '3':
                return
    
    def exibir_perfil(self) -> None:
        """Exibe perfil do usuário logado"""
        while True:
            self._limpar_tela()
            usuario = self.usuarios[self.usuario_logado]
            
            print("=" * 60)
            print("👤 MEU PERFIL")
            print("=" * 60)
            print(f"\n👤 {usuario['nome']} (@{self.usuario_logado})")
            print(f"💼 {usuario['titulo']}")
            print(f"📝 {usuario['bio']}")
            print(f"📅 {usuario['data_criacao']}")
            print(f"\n🔗 Conexões: {len(self.conexoes[self.usuario_logado])}")
            print("\n1️⃣  - Editar | 2️⃣  - Voltar")
            
            if input("\nOpção: ").strip() == '1':
                self._editar_perfil()
            else:
                return
    
    def _editar_perfil(self) -> None:
        """Edita perfil do usuário"""
        self._limpar_tela()
        usuario = self.usuarios[self.usuario_logado]
        
        print("=" * 60)
        print("✏️  EDITAR PERFIL")
        print("=" * 60)
        print(f"\n1️⃣  Título: {usuario['titulo']}")
        print(f"2️⃣  Bio: {usuario['bio']}")
        print("3️⃣  Voltar")
        
        opcao = input("\nEditar: ").strip()
        if opcao == '1':
            novo = input("\nNovo título: ").strip()
            if novo:
                usuario['titulo'] = novo
                self._salvar_dados()
                print("✅ Atualizado!")
        elif opcao == '2':
            novo = input(f"\nNova bio (máx {self.MAX_BIO_LEN}): ").strip()[:self.MAX_BIO_LEN]
            if novo:
                usuario['bio'] = novo
                self._salvar_dados()
                print("✅ Atualizado!")
        
        input("\n👉 ENTER...")
    
    def buscar_usuarios(self) -> None:
        """Busca usuários para conectar"""
        self._limpar_tela()
        termo = input("=" * 60 + "\n🔍 BUSCAR USUÁRIOS\n" + "=" * 60 + "\nNome/username: ").strip().lower()
        
        if not termo:
            print("⚠️  Vazio")
            input("\n👉 ENTER...")
            return
        
        resultados = list(self._buscar_usuarios(termo))
        if not resultados:
            print("❌ Nenhum encontrado")
            input("\n👉 ENTER...")
            return
        
        self._limpar_tela()
        print("=" * 60)
        print("👥 RESULTADOS")
        print("=" * 60)
        
        for i, (username, dados) in enumerate(resultados, 1):
            print(f"\n{i}. {dados['nome']} (@{username})")
            print(f"   💼 {dados['titulo']}")
        
        if len(resultados) == 1:
            username = resultados[0][0]
            if username != self.usuario_logado:
                if input("\nAdicionar? (S/N): ").strip().upper() == 'S':
                    self.adicionar_conexao(username)
        
        input("\n👉 ENTER...")
    
    def adicionar_conexao(self, username_alvo: str) -> None:
        """Adiciona conexão"""
        if username_alvo not in self.usuarios or username_alvo == self.usuario_logado:
            print("❌ Inválido")
            return
        
        if username_alvo in self.conexoes[self.usuario_logado]:
            print("⚠️  Já conectados")
            return
        
        self.conexoes[self.usuario_logado].append(username_alvo)
        if self.usuario_logado not in self.conexoes[username_alvo]:
            self.conexoes[username_alvo].append(self.usuario_logado)
        
        if username_alvo not in self.usuarios[self.usuario_logado]['seguindo']:
            self.usuarios[self.usuario_logado]['seguindo'].append(username_alvo)
        if self.usuario_logado not in self.usuarios[username_alvo]['seguidores']:
            self.usuarios[username_alvo]['seguidores'].append(self.usuario_logado)
        
        self._salvar_dados()
        print("✅ Conectado!")
    
    def listar_conexoes(self) -> None:
        """Lista conexões"""
        self._limpar_tela()
        conexoes = self.conexoes[self.usuario_logado]
        
        print("=" * 60)
        print("🔗 MINHAS CONEXÕES")
        print("=" * 60)
        
        if not conexoes:
            print("\n⚠️  Sem conexões")
        else:
            print(f"\n✅ {len(conexoes)} conexão(ões):\n")
            for i, username in enumerate(conexoes, 1):
                dados = self.usuarios[username]
                print(f"{i}. {dados['nome']} (@{username}) - {dados['titulo']}")
        
        input("\n👉 ENTER...")
    
    def criar_post(self) -> None:
        """Cria novo post"""
        self._limpar_tela()
        print("=" * 60)
        print("✍️  CRIAR POST")
        print("=" * 60)
        print(f"\nMáx {self.MAX_POST_LEN} caracteres (SAIR para cancelar)\n")
        
        linhas = []
        while True:
            linha = input()
            if linha.strip().upper() == 'SAIR':
                print("⚠️  Cancelado")
                input("\n👉 ENTER...")
                return
            linhas.append(linha)
            if len('\n'.join(linhas)) >= self.MAX_POST_LEN:
                break
        
        conteudo = '\n'.join(linhas).strip()
        if len(conteudo) < self.MIN_POST_LEN:
            print(f"❌ Mín {self.MIN_POST_LEN} caracteres")
            input("\n👉 ENTER...")
            return
        
        novo_id = max([p['id'] for p in self.posts], default=0) + 1
        novo_post = {
            'id': novo_id, 'usuario': self.usuario_logado,
            'autor_nome': self.usuarios[self.usuario_logado]['nome'],
            'conteudo': conteudo[:self.MAX_POST_LEN],
            'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'likes': [], 'comentarios': []
        }
        
        self.posts.insert(0, novo_post)
        self._salvar_dados()
        print("\n✅ PUBLICADO!")
        input("\n👉 ENTER...")
    
    def feed(self) -> None:
        """Exibe feed de posts"""
        if not self.posts:
            self._limpar_tela()
            print("⚠️  Sem posts")
            input("\n� ENTER...")
            return
        
        indice = 0
        while indice < len(self.posts):
            self._limpar_tela()
            post = self.posts[indice]
            
            print("=" * 60)
            print("📰 FEED")
            print("=" * 60)
            print(f"\nPost {indice + 1}/{len(self.posts)}\n")
            print("-" * 60)
            print(f"{post['autor_nome']} (@{post['usuario']})")
            print(f"📅 {post['data']}\n\n{post['conteudo']}\n")
            print("-" * 60)
            print(f"❤️  {len(post['likes'])} | 💬 {len(post['comentarios'])}")
            
            if post['comentarios']:
                print("\n💬:")
                for i, com in enumerate(post['comentarios'][:2], 1):
                    print(f"  {i}. {com['nome']}: {com['texto'][:40]}...")
            
            print("\n" + "-" * 60)
            
            if post['usuario'] != self.usuario_logado:
                print("1=Curtir | 2=Comentar | 3=Sair | </>=Nav")
                opcao = input("\nOpção: ").strip()
                
                if opcao == '1':
                    self._curtir_post(post)
                elif opcao == '2':
                    self._comentar_post(post)
                elif opcao == '3':
                    return
                elif opcao in ['a', '4']:
                    indice = max(0, indice - 1)
                else:
                    indice = min(len(self.posts) - 1, indice + 1)
            else:
                print("1=Deletar | 2=Sair | </>=Nav")
                opcao = input("\nOpção: ").strip()
                
                if opcao == '1':
                    if input("Certeza? (S/N): ").upper() == 'S':
                        self.posts.pop(indice)
                        self._salvar_dados()
                        indice = min(indice, len(self.posts) - 1) if self.posts else 0
                elif opcao == '2':
                    return
                elif opcao in ['a', '4']:
                    indice = max(0, indice - 1)
                else:
                    indice = min(len(self.posts) - 1, indice + 1)
    
    def _curtir_post(self, post: Dict) -> None:
        """Curte/descurte post"""
        if self.usuario_logado in post['likes']:
            post['likes'].remove(self.usuario_logado)
            print("💔 Removido")
        else:
            post['likes'].append(self.usuario_logado)
            print("❤️  Curtido!")
        self._salvar_dados()
        input("\n👉 ENTER...")
    
    def _comentar_post(self, post: Dict) -> None:
        """Adiciona comentário"""
        com = input("\n📝 Comentário (máx 200): ").strip()[:self.MAX_COMENTARIO]
        if len(com) < 2:
            print("⚠️  Muito curto")
            return
        
        post['comentarios'].append({
            'usuario': self.usuario_logado,
            'nome': self.usuarios[self.usuario_logado]['nome'],
            'texto': com,
            'data': datetime.now().strftime('%d/%m/%Y %H:%M')
        })
        self._salvar_dados()
        print("✅ Adicionado!")
        input("\n👉 ENTER...")
    
    def menu_principal(self) -> None:
        """Menu principal"""
        while not self.usuario_logado:
            self._limpar_tela()
            print("=" * 60)
            print("🌐 PROFESSIONALNET")
            print("=" * 60)
            print("\n1️⃣  - Registrar")
            print("2️⃣  - Login")
            print("3️⃣  - Ver perfis (sem login)")
            print("4️⃣  - Sair")
            
            opcao = input("\nOpção: ").strip()
            
            if opcao == '1':
                self.registrar_usuario()
            elif opcao == '2':
                if self.fazer_login():
                    break
            elif opcao == '3':
                self.visualizar_perfil_publico()
            elif opcao == '4':
                print("\n👋 Até logo!")
                return
    
    def menu_usuario(self) -> None:
        """Menu do usuário logado"""
        while self.usuario_logado:
            usuario = self.usuarios[self.usuario_logado]
            self._limpar_tela()
            print("=" * 60)
            print(f"🌐 Bem-vindo, {usuario['nome']}")
            print("=" * 60)
            print("\n1️⃣  - Meu perfil")
            print("2️⃣  - Buscar usuários")
            print("3️⃣  - Minhas conexões")
            print("4️⃣  - Feed")
            print("5️⃣  - Novo post")
            print("6️⃣  - Logout")
            
            opcao = input("\nOpção: ").strip()
            
            if opcao == '1':
                self.exibir_perfil()
            elif opcao == '2':
                self.buscar_usuarios()
            elif opcao == '3':
                self.listar_conexoes()
            elif opcao == '4':
                self.feed()
            elif opcao == '5':
                self.criar_post()
            elif opcao == '6':
                if input("\nSair? (S/N): ").upper() == 'S':
                    print(f"\n👋 Até logo, {usuario['nome']}!")
                    self.usuario_logado = None
                    input("\n👉 ENTER...")
    
    def iniciar(self) -> None:
        """Inicia o sistema"""
        try:
            self._limpar_tela()
            print("\n" + "╔" + "=" * 58 + "╗")
            print("║" + "🌐 BEM-VINDO AO PROFESSIONALNET 🌐".center(56) + "║")
            print("║" + "Rede Social Profissional".center(58) + "║")
            print("╚" + "=" * 58 + "╝\n")
            
            input("👉 ENTER para começar...")
            
            self.menu_principal()
            self.menu_usuario()
            
            print("\n✅ Sistema finalizado!")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrompido")
        except Exception as e:
            print(f"\n❌ Erro: {e}")


def main():
    """Função principal"""
    try:
        sistema = ProfessionalNet()
        sistema.iniciar()
    except Exception as e:
        print(f"❌ Erro ao iniciar o sistema: {e}")


if __name__ == "__main__":
    main()

