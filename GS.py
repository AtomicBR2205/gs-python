"""
SISTEMA LINKEDIN EM SPA - REDES SOCIAIS PROFISSIONAIS
Autor: Sistema de Gestão
Data: 2025
Descrição: Sistema completo de rede social profissional com validações, 
tratamento de exceções e estrutura de menu intuitiva.
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any


class LinkedInSPA:
    """Classe principal do sistema LinkedIn SPA"""
    
    def __init__(self):
        """Inicializa o sistema com banco de dados em dicionários"""
        self.usuarios = {}  # Armazena dados dos usuários
        self.conexoes = {}  # Armazena conexões entre usuários
        self.posts = []  # Armazena posts (id_usuario, conteúdo, data, likes)
        self.usuario_logado = None  # Usuário atualmente logado
        self._inicializar_dados_teste()  # Carrega dados de teste
        
    def _inicializar_dados_teste(self) -> None:
        """Inicializa com dados de teste para demonstração"""
        try:
            self.usuarios = {
                'usuario1': {
                    'nome': 'João Silva',
                    'email': 'joao@example.com',
                    'senha': '123456',
                    'titulo': 'Desenvolvedor Python',
                    'bio': 'Apaixonado por programação',
                    'data_criacao': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'seguidores': [],
                    'seguindo': []
                },
                'usuario2': {
                    'nome': 'Maria Santos',
                    'email': 'maria@example.com',
                    'senha': '123456',
                    'titulo': 'Designer UX/UI',
                    'bio': 'Criando experiências incríveis',
                    'data_criacao': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'seguidores': [],
                    'seguindo': []
                }
            }
            
            # Inicializa conexões
            self.conexoes = {
                'usuario1': ['usuario2'],
                'usuario2': ['usuario1']
            }
            
            # Inicializa posts de teste
            self.posts = [
                {
                    'id': 1,
                    'usuario': 'usuario1',
                    'autor_nome': 'João Silva',
                    'conteudo': 'Bem-vindo ao LinkedIn SPA! 🚀',
                    'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'likes': [],
                    'comentarios': []
                },
                {
                    'id': 2,
                    'usuario': 'usuario2',
                    'autor_nome': 'Maria Santos',
                    'conteudo': 'Adorando este novo sistema de rede social! 💼',
                    'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'likes': ['usuario1'],
                    'comentarios': []
                }
            ]
        except Exception as e:
            print(f"Erro ao inicializar dados de teste: {e}")
    
    @staticmethod
    def _limpar_tela() -> None:
        """Limpa a tela do console"""
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except Exception as e:
            print(f"Erro ao limpar tela: {e}")
    
    @staticmethod
    def _validar_email(email: str) -> bool:
        """Valida formato de email"""
        try:
            padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(padrao, email))
        except Exception as e:
            print(f"Erro na validação de email: {e}")
            return False
    
    @staticmethod
    def _validar_senha(senha: str) -> Tuple[bool, str]:
        """Valida força da senha"""
        try:
            if len(senha) < 6:
                return False, "Senha deve ter pelo menos 6 caracteres"
            if not any(c.isupper() for c in senha):
                return False, "Senha deve conter letra maiúscula"
            if not any(c.isdigit() for c in senha):
                return False, "Senha deve conter números"
            return True, "Senha forte"
        except Exception as e:
            print(f"Erro na validação de senha: {e}")
            return False, "Erro na validação"
    
    @staticmethod
    def _validar_username(username: str) -> Tuple[bool, str]:
        """Valida username"""
        try:
            if len(username) < 3:
                return False, "Username deve ter pelo menos 3 caracteres"
            if not re.match(r'^[a-zA-Z0-9_]+$', username):
                return False, "Username pode conter apenas letras, números e underscore"
            return True, "Username válido"
        except Exception as e:
            print(f"Erro na validação de username: {e}")
            return False, "Erro na validação"
    
    def registrar_usuario(self) -> None:
        """Registra um novo usuário no sistema"""
        self._limpar_tela()
        print("=" * 60)
        print("📝 REGISTRO DE NOVO USUÁRIO")
        print("=" * 60)
        
        try:
            # Validar username
            while True:
                username = input("\n👤 Digite o nome de usuário (username): ").strip()
                valido, mensagem = self._validar_username(username)
                
                if not valido:
                    print(f"❌ {mensagem}")
                    continue
                
                if username in self.usuarios:
                    print("❌ Username já está em uso. Tente outro.")
                    continue
                
                break
            
            # Validar email
            while True:
                email = input("\n📧 Digite seu email: ").strip()
                if not self._validar_email(email):
                    print("❌ Email inválido. Use o formato: usuario@exemplo.com")
                    continue
                
                if any(u['email'] == email for u in self.usuarios.values()):
                    print("❌ Email já cadastrado no sistema.")
                    continue
                
                break
            
            # Validar senha
            while True:
                senha = input("\n🔒 Digite sua senha: ").strip()
                valido, mensagem = self._validar_senha(senha)
                
                if not valido:
                    print(f"❌ {mensagem}")
                    print("   Requisitos: mín. 6 caracteres, 1 maiúscula, 1 número")
                    continue
                
                confirmacao = input("   Confirme a senha: ").strip()
                if senha != confirmacao:
                    print("❌ As senhas não conferem.")
                    continue
                
                break
            
            # Coletar dados adicionais
            nome_completo = input("\n✍️  Nome completo: ").strip()
            if not nome_completo or len(nome_completo) < 3:
                print("❌ Nome deve ter pelo menos 3 caracteres.")
                return
            
            titulo = input("💼 Título profissional (ex: Desenvolvedor Python): ").strip()
            bio = input("📝 Biografia (máx 200 caracteres): ").strip()[:200]
            
            # Criar novo usuário
            self.usuarios[username] = {
                'nome': nome_completo,
                'email': email,
                'senha': senha,
                'titulo': titulo if titulo else "Profissional",
                'bio': bio if bio else "Sem bio informada",
                'data_criacao': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'seguidores': [],
                'seguindo': []
            }
            
            self.conexoes[username] = []
            
            print("\n✅ USUÁRIO REGISTRADO COM SUCESSO!")
            print(f"📌 Bem-vindo, {nome_completo}!")
            input("\n👉 Pressione ENTER para continuar...")
            
        except KeyboardInterrupt:
            print("\n⚠️  Operação cancelada pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro durante registro: {e}")
    
    def fazer_login(self) -> bool:
        """Realiza login do usuário"""
        self._limpar_tela()
        print("=" * 60)
        print("🔐 LOGIN")
        print("=" * 60)
        
        try:
            username = input("\n👤 Username: ").strip()
            senha = input("🔒 Senha: ").strip()
            
            if username not in self.usuarios:
                print("❌ Usuário não encontrado.")
                input("\n👉 Pressione ENTER para voltar...")
                return False
            
            if self.usuarios[username]['senha'] != senha:
                print("❌ Senha incorreta.")
                input("\n👉 Pressione ENTER para voltar...")
                return False
            
            self.usuario_logado = username
            print(f"\n✅ Bem-vindo, {self.usuarios[username]['nome']}!")
            input("\n👉 Pressione ENTER para continuar...")
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️  Login cancelado.")
            return False
        except Exception as e:
            print(f"\n❌ Erro no login: {e}")
            return False
    
    def exibir_perfil(self, username: Optional[str] = None) -> None:
        """Exibe o perfil de um usuário"""
        self._limpar_tela()
        
        try:
            usr = username if username else self.usuario_logado
            
            if usr not in self.usuarios:
                print("❌ Usuário não encontrado.")
                input("\n👉 Pressione ENTER para voltar...")
                return
            
            usuario = self.usuarios[usr]
            
            print("=" * 60)
            print("👤 PERFIL DO USUÁRIO")
            print("=" * 60)
            print(f"\n👤 Nome: {usuario['nome']}")
            print(f"📧 Email: {usuario['email']}")
            print(f"💼 Título: {usuario['titulo']}")
            print(f"📝 Bio: {usuario['bio']}")
            print(f"📅 Membro desde: {usuario['data_criacao']}")
            print(f"\n🔗 Conexões: {len(self.conexoes.get(usr, []))}")
            print(f"👥 Seguidores: {len(usuario['seguidores'])}")
            print(f"📌 Seguindo: {len(usuario['seguindo'])}")
            
            # Se é o perfil do próprio usuário, mostrar opções de edição
            if usr == self.usuario_logado:
                print("\n" + "-" * 60)
                print("📋 OPÇÕES:")
                print("1️⃣  - Editar perfil")
                print("2️⃣  - Voltar")
                
                opcao = input("\nEscolha uma opção: ").strip()
                
                if opcao == '1':
                    self._editar_perfil()
            else:
                input("\n👉 Pressione ENTER para voltar...")
            
        except Exception as e:
            print(f"❌ Erro ao exibir perfil: {e}")
            input("\n👉 Pressione ENTER para voltar...")
    
    def _editar_perfil(self) -> None:
        """Edita o perfil do usuário logado"""
        self._limpar_tela()
        
        try:
            usuario = self.usuarios[self.usuario_logado]
            
            print("=" * 60)
            print("✏️  EDITAR PERFIL")
            print("=" * 60)
            print(f"\n1️⃣  - Título profissional: {usuario['titulo']}")
            print(f"2️⃣  - Biografia: {usuario['bio']}")
            print(f"3️⃣  - Voltar")
            
            opcao = input("\nO que deseja editar? ").strip()
            
            if opcao == '1':
                novo_titulo = input("\nNovo título profissional: ").strip()
                if novo_titulo:
                    usuario['titulo'] = novo_titulo
                    print("✅ Título atualizado com sucesso!")
            
            elif opcao == '2':
                nova_bio = input("\nNova biografia (máx 200 caracteres): ").strip()[:200]
                if nova_bio:
                    usuario['bio'] = nova_bio
                    print("✅ Biografia atualizada com sucesso!")
            
            input("\n👉 Pressione ENTER para continuar...")
            
        except Exception as e:
            print(f"❌ Erro ao editar perfil: {e}")
    
    def buscar_usuarios(self) -> None:
        """Busca por usuários no sistema"""
        self._limpar_tela()
        
        try:
            print("=" * 60)
            print("🔍 BUSCAR USUÁRIOS")
            print("=" * 60)
            
            termo = input("\nDigite o nome ou username para buscar: ").strip().lower()
            
            if not termo:
                print("⚠️  Digite algum termo de busca.")
                input("\n👉 Pressione ENTER para voltar...")
                return
            
            resultados = [
                (usr, dados) for usr, dados in self.usuarios.items()
                if termo in usr.lower() or termo in dados['nome'].lower()
            ]
            
            if not resultados:
                print(f"\n❌ Nenhum usuário encontrado com '{termo}'.")
            else:
                print(f"\n✅ {len(resultados)} usuário(s) encontrado(s):\n")
                
                for i, (username, dados) in enumerate(resultados, 1):
                    print(f"{i}️⃣  {dados['nome']} (@{username})")
                    print(f"   💼 {dados['titulo']}")
                    print(f"   📝 {dados['bio'][:50]}...")
                    print()
                
                # Opção de adicionar como conexão
                if len(resultados) == 1:
                    username = resultados[0][0]
                    if username != self.usuario_logado:
                        opcao = input("Deseja adicionar esta pessoa? (S/N): ").strip().upper()
                        if opcao == 'S':
                            self.adicionar_conexao(username)
            
            input("\n👉 Pressione ENTER para voltar...")
            
        except Exception as e:
            print(f"❌ Erro na busca: {e}")
            input("\n👉 Pressione ENTER para voltar...")
    
    def adicionar_conexao(self, username_alvo: str) -> None:
        """Adiciona um usuário como conexão"""
        try:
            if username_alvo not in self.usuarios:
                print("❌ Usuário não encontrado.")
                return
            
            if username_alvo == self.usuario_logado:
                print("❌ Você não pode conectar-se a si mesmo.")
                return
            
            if username_alvo in self.conexoes[self.usuario_logado]:
                print("⚠️  Vocês já são conexões.")
                return
            
            # Adicionar conexão
            self.conexoes[self.usuario_logado].append(username_alvo)
            if self.usuario_logado not in self.conexoes[username_alvo]:
                self.conexoes[username_alvo].append(self.usuario_logado)
            
            # Adicionar seguidor/seguindo
            self.usuarios[self.usuario_logado]['seguindo'].append(username_alvo)
            self.usuarios[username_alvo]['seguidores'].append(self.usuario_logado)
            
            print(f"✅ Conexão adicionada com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao adicionar conexão: {e}")
    
    def listar_conexoes(self) -> None:
        """Lista as conexões do usuário"""
        self._limpar_tela()
        
        try:
            conexoes = self.conexoes.get(self.usuario_logado, [])
            
            print("=" * 60)
            print("🔗 MINHAS CONEXÕES")
            print("=" * 60)
            
            if not conexoes:
                print("\n⚠️  Você ainda não tem conexões.")
                print("   Vá até 'Buscar Usuários' para fazer novas conexões!")
            else:
                print(f"\n✅ Você tem {len(conexoes)} conexão(ões):\n")
                
                for i, username in enumerate(conexoes, 1):
                    usuario = self.usuarios[username]
                    print(f"{i}️⃣  {usuario['nome']} (@{username})")
                    print(f"   💼 {usuario['titulo']}")
                    print(f"   📍 {len(self.conexoes.get(username, []))} conexões")
                    print()
            
            input("\n👉 Pressione ENTER para voltar...")
            
        except Exception as e:
            print(f"❌ Erro ao listar conexões: {e}")
            input("\n👉 Pressione ENTER para voltar...")
    
    def criar_post(self) -> None:
        """Cria um novo post"""
        self._limpar_tela()
        
        try:
            print("=" * 60)
            print("✍️  CRIAR POST")
            print("=" * 60)
            print("\n(Máximo 500 caracteres)")
            print("(Digite 'SAIR' em uma linha vazia para cancelar)\n")
            
            linhas = []
            while True:
                linha = input()
                
                if linha.strip().upper() == 'SAIR':
                    print("⚠️  Post cancelado.")
                    input("\n👉 Pressione ENTER para voltar...")
                    return
                
                linhas.append(linha)
                
                if len('\n'.join(linhas)) >= 500:
                    break
                
                if not linha.strip():
                    confirmacao = input("Deseja publicar agora? (S/N): ").strip().upper()
                    if confirmacao == 'S':
                        break
                    linhas.append('')
            
            conteudo = '\n'.join(linhas).strip()
            
            if not conteudo or len(conteudo) < 5:
                print("❌ Post deve ter pelo menos 5 caracteres.")
                input("\n👉 Pressione ENTER para voltar...")
                return
            
            # Criar post
            novo_id = max([p['id'] for p in self.posts], default=0) + 1
            
            novo_post = {
                'id': novo_id,
                'usuario': self.usuario_logado,
                'autor_nome': self.usuarios[self.usuario_logado]['nome'],
                'conteudo': conteudo[:500],
                'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'likes': [],
                'comentarios': []
            }
            
            self.posts.insert(0, novo_post)  # Adiciona no início (mais recente)
            
            print("\n✅ POST PUBLICADO COM SUCESSO!")
            input("\n👉 Pressione ENTER para continuar...")
            
        except Exception as e:
            print(f"❌ Erro ao criar post: {e}")
            input("\n👉 Pressione ENTER para voltar...")
    
    def feed(self) -> None:
        """Exibe o feed de posts"""
        self._limpar_tela()
        
        try:
            print("=" * 60)
            print("📰 FEED DE POSTS")
            print("=" * 60)
            
            if not self.posts:
                print("\n⚠️  Nenhum post disponível ainda.")
                input("\n👉 Pressione ENTER para voltar...")
                return
            
            print(f"\n✅ Total de {len(self.posts)} post(s)\n")
            
            for i, post in enumerate(self.posts, 1):
                print("-" * 60)
                print(f"{i}️⃣  {post['autor_nome']} (@{post['usuario']})")
                print(f"   📅 {post['data']}")
                print(f"\n   {post['conteudo']}\n")
                print(f"   ❤️  Likes: {len(post['likes'])} | 💬 Comentários: {len(post['comentarios'])}")
                
                # Opções de interação
                if post['usuario'] != self.usuario_logado:
                    print(f"\n   1️⃣  - Curtir | 2️⃣  - Comentar | 3️⃣  - Continuar lendo")
                    
                    opcao = input("   Opção: ").strip()
                    
                    if opcao == '1':
                        self._curtir_post(post)
                    elif opcao == '2':
                        self._comentar_post(post)
                    elif opcao == '3':
                        continue
                    else:
                        print("   ⚠️  Opção inválida.")
                else:
                    print(f"\n   📌 Seu post | 1️⃣  - Deletar | 2️⃣  - Continuar")
                    
                    opcao = input("   Opção: ").strip()
                    
                    if opcao == '1':
                        self._deletar_post(post['id'])
                    elif opcao == '2':
                        continue
                
                print()
            
            input("\n👉 Pressione ENTER para voltar...")
            
        except Exception as e:
            print(f"❌ Erro ao exibir feed: {e}")
            input("\n👉 Pressione ENTER para voltar...")
    
    def _curtir_post(self, post: Dict[str, Any]) -> None:
        """Curte um post"""
        try:
            if self.usuario_logado in post['likes']:
                post['likes'].remove(self.usuario_logado)
                print("\n   💔 Like removido.")
            else:
                post['likes'].append(self.usuario_logado)
                print("\n   ❤️  Post curtido com sucesso!")
        except Exception as e:
            print(f"   ❌ Erro ao curtir post: {e}")
    
    def _comentar_post(self, post: Dict[str, Any]) -> None:
        """Adiciona um comentário em um post"""
        try:
            comentario = input("\n   📝 Digite seu comentário (máx 200 caracteres): ").strip()[:200]
            
            if not comentario or len(comentario) < 2:
                print("   ⚠️  Comentário muito curto.")
                return
            
            novo_comentario = {
                'usuario': self.usuario_logado,
                'nome': self.usuarios[self.usuario_logado]['nome'],
                'texto': comentario,
                'data': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
            
            post['comentarios'].append(novo_comentario)
            print("   ✅ Comentário adicionado com sucesso!")
            
        except Exception as e:
            print(f"   ❌ Erro ao comentar: {e}")
    
    def _deletar_post(self, post_id: int) -> None:
        """Deleta um post do usuário"""
        try:
            post = next((p for p in self.posts if p['id'] == post_id), None)
            
            if not post or post['usuario'] != self.usuario_logado:
                print("   ❌ Você não pode deletar este post.")
                return
            
            confirmacao = input("   ⚠️  Tem certeza? (S/N): ").strip().upper()
            
            if confirmacao == 'S':
                self.posts.remove(post)
                print("   ✅ Post deletado com sucesso!")
            else:
                print("   ⚠️  Deleção cancelada.")
        
        except Exception as e:
            print(f"   ❌ Erro ao deletar post: {e}")
    
    def menu_principal(self) -> None:
        """Exibe o menu principal do sistema"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print("🌐 LINKEDIN SPA - REDE SOCIAL PROFISSIONAL")
            print("=" * 60)
            
            if not self.usuario_logado:
                print("\n📌 MENU PRINCIPAL")
                print("1️⃣  - Registrar")
                print("2️⃣  - Login")
                print("3️⃣  - Sair")
                
                try:
                    opcao = input("\nEscolha uma opção: ").strip()
                    
                    if opcao == '1':
                        self.registrar_usuario()
                    elif opcao == '2':
                        if self.fazer_login():
                            break
                    elif opcao == '3':
                        print("\n👋 Obrigado por usar o LinkedIn SPA!")
                        print("   Até logo!")
                        return
                    else:
                        print("❌ Opção inválida.")
                        input("\n👉 Pressione ENTER para tentar novamente...")
                        
                except KeyboardInterrupt:
                    print("\n⚠️  Operação cancelada.")
                except Exception as e:
                    print(f"❌ Erro: {e}")
            else:
                break
    
    def menu_usuario(self) -> None:
        """Menu do usuário logado"""
        while self.usuario_logado:
            self._limpar_tela()
            usuario = self.usuarios[self.usuario_logado]
            
            print("=" * 60)
            print(f"🌐 LINKEDIN SPA - Bem-vindo, {usuario['nome']}")
            print("=" * 60)
            print("\n📋 MENU PRINCIPAL")
            print("1️⃣  - Ver meu perfil")
            print("2️⃣  - Buscar usuários")
            print("3️⃣  - Minhas conexões")
            print("4️⃣  - Feed de posts")
            print("5️⃣  - Criar novo post")
            print("6️⃣  - Logout")
            
            try:
                opcao = input("\nEscolha uma opção: ").strip()
                
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
                    confirmacao = input("\nTem certeza que deseja sair? (S/N): ").strip().upper()
                    if confirmacao == 'S':
                        print("\n👋 Até logo, " + usuario['nome'] + "!")
                        self.usuario_logado = None
                        input("\n👉 Pressione ENTER para continuar...")
                        break
                else:
                    print("❌ Opção inválida.")
                    input("\n👉 Pressione ENTER para tentar novamente...")
                    
            except KeyboardInterrupt:
                print("\n⚠️  Operação cancelada.")
                input("\n👉 Pressione ENTER para continuar...")
            except Exception as e:
                print(f"❌ Erro: {e}")
                input("\n👉 Pressione ENTER para tentar novamente...")
    
    def iniciar(self) -> None:
        """Inicia o sistema"""
        try:
            self._limpar_tela()
            print("\n" * 2)
            print("╔" + "=" * 58 + "╗")
            print("║" + " " * 58 + "║")
            print("║" + "    🌐 BEM-VINDO AO LINKEDIN SPA 🌐".center(58) + "║")
            print("║" + "  Rede Social Profissional em Python".center(58) + "║")
            print("║" + " " * 58 + "║")
            print("╚" + "=" * 58 + "╝")
            print("\n")
            
            input("👉 Pressione ENTER para começar...")
            
            self.menu_principal()
            self.menu_usuario()
            
            print("\n✅ Sistema finalizado com sucesso!")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Sistema interrompido pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro fatal: {e}")


def main():
    """Função principal"""
    try:
        sistema = LinkedInSPA()
        sistema.iniciar()
    except Exception as e:
        print(f"❌ Erro ao iniciar o sistema: {e}")


if __name__ == "__main__":
    main()

