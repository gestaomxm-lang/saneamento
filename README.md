# Saneamento App - Plataforma de Gestão

Uma aplicação moderna para gerenciamento de projetos de saneamento com dashboard interativo, relatórios em tempo real e análise de dados.

## 🚀 Características

- **Dashboard Interativo**: Visualize suas métricas em tempo real
- **Gráficos Dinâmicos**: Análise com gráficos de barras, linhas e pizza
- **Gerenciamento de Usuários**: Sistema completo de usuários
- **Configurações Personalizáveis**: Customize sua experiência
- **Design Responsivo**: Funciona perfeitamente em qualquer dispositivo
- **Performance Otimizada**: Carregamento rápido e fluido

## 🛠️ Stack Tecnológico

- **Next.js 14**: Framework React moderno
- **TypeScript**: Tipagem estática para mais segurança
- **Tailwind CSS**: Estilização utilitária
- **Recharts**: Biblioteca de gráficos interativos
- **Lucide React**: Ícones modernos

## 📦 Instalação Local

```bash
# Clonar o repositório
git clone <seu-repo>
cd saneamento-app

# Instalar dependências
npm install

# Executar em desenvolvimento
npm run dev
```

Acesse `http://localhost:3000` no seu navegador.

## 🚀 Deploy no Vercel

### Pré-requisitos
- Conta no [Vercel](https://vercel.com)
- Código hospedado no [GitHub](https://github.com)

### Passos para Deploy

1. **Fazer push do código para GitHub**
   ```bash
   git add .
   git commit -m "Inicial commit"
   git push origin main
   ```

2. **Conectar ao Vercel**
   - Acesse [vercel.com](https://vercel.com)
   - Clique em "New Project"
   - Selecione seu repositório GitHub
   - Vercel detectará automaticamente que é Next.js
   - Clique em "Deploy"

3. **Configurações Recomendadas no Vercel**
   - **Root Directory**: `.` (raiz)
   - **Framework**: Next.js
   - **Build Command**: `npm run build` (automático)
   - **Output Directory**: `.next` (automático)

4. **Variáveis de Ambiente** (se necessário)
   - Configure em "Settings" → "Environment Variables"

## 📁 Estrutura do Projeto

```
saneamento-app/
├── app/
│   ├── layout.tsx          # Layout principal
│   ├── globals.css         # Estilos globais
│   ├── page.tsx            # Home page
│   ├── relatorios/         # Página de relatórios
│   ├── usuarios/           # Página de usuários
│   └── config/             # Página de configurações
├── components/
│   ├── Navbar.tsx          # Barra de navegação
│   ├── Charts.tsx          # Componentes de gráficos
│   └── StatCard.tsx        # Cards de estatísticas
├── public/                 # Arquivos estáticos
├── package.json
├── tailwind.config.ts
├── next.config.js
└── tsconfig.json
```

## 🎨 Paleta de Cores

- **Navy**: `#3f87bc` (Cor principal)
- **Teal**: `#22c55e` (Cor secundária)
- **Branco**: `#ffffff` (Fundo)
- **Cinza**: `#f3f4f6` (Destaques)

## 📝 Páginas Disponíveis

- **/** - Dashboard principal com estatísticas e gráficos
- **/relatorios** - Relatórios detalhados
- **/usuarios** - Gerenciamento de usuários
- **/config** - Configurações da plataforma

## 🔧 Comandos Disponíveis

```bash
npm run dev      # Inicia servidor de desenvolvimento
npm run build    # Cria build de produção
npm start        # Inicia servidor de produção
npm run lint     # Executa linter
```

## 📱 Responsividade

A aplicação é totalmente responsiva com breakpoints:
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🔒 Segurança

- Next.js com proteção built-in contra XSS
- Tipagem TypeScript para evitar erros
- Headers de segurança configurados
- CSRF protection incluído

## 📧 Suporte

Para problemas ou sugestões, abra uma issue no repositório.

## 📄 Licença

Este projeto está sob a licença MIT.

---

Desenvolvido com ❤️ usando Next.js e Tailwind CSS
