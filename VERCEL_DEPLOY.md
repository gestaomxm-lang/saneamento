# Next.js Vercel Deployment

Este projeto é um Next.js app pronto para deploy no Vercel.

## Deploy Rápido

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyour-username%2Fsaneamento-app)

## Instruções de Deploy Local

### 1. Preparar o Código

```powershell
# Navegar até a pasta do projeto
cd "C:\Users\MEUCOMPUTADOR\Desktop\saniô"

# Inicializar repositório Git (se ainda não estiver)
git init
git add .
git commit -m "Initial commit - Saneamento App"
```

### 2. Fazer Push para GitHub

```powershell
# Adicionar remote (substitua pela sua URL)
git remote add origin https://github.com/seu-usuario/saneamento-app.git
git branch -M main
git push -u origin main
```

### 3. Conectar ao Vercel

1. Acesse https://vercel.com
2. Clique em "New Project"
3. Selecione "Import Git Repository"
4. Escolha seu repositório GitHub
5. Clique em "Deploy"

## Variáveis de Ambiente

Se precisar adicionar variáveis de ambiente no Vercel:

1. Acesse seu projeto no Vercel
2. Vá para "Settings" → "Environment Variables"
3. Adicione suas variáveis (ex: API keys, URLs, etc)

## Monitoramento

- **Build Logs**: Disponível na aba "Deployments"
- **Real-time Analytics**: Em "Analytics"
- **Error Tracking**: Em "Monitoring"

## Troubleshooting

### Build falha
- Verifique se todas as dependências estão em `package.json`
- Confirme que não há erros de TypeScript

### Aplicação lenta
- Verifique analytics no Vercel
- Otimize imagens e cache

### Problemas de importação
- Verifique o path alias em `tsconfig.json`
- Certifique-se que `@/` aponta para o diretório correto
