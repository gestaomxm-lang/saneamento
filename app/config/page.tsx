import Navbar from '@/components/Navbar'
import { Settings, Bell, Lock, Eye } from 'lucide-react'

export default function Config() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
      <Navbar />

      <section className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-4xl font-bold gradient-text mb-12 flex items-center gap-3">
          <Settings size={32} />
          Configurações
        </h1>

        <div className="space-y-6">
          {/* Perfil */}
          <div className="glass-effect p-8 card-hover">
            <h2 className="text-2xl font-bold text-navy-900 mb-6 flex items-center gap-3">
              <Eye size={24} />
              Perfil
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Nome</label>
                <input
                  type="text"
                  defaultValue="João Silva"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-navy-500 focus:border-transparent outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                <input
                  type="email"
                  defaultValue="joao@example.com"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-navy-500 focus:border-transparent outline-none"
                />
              </div>
              <button className="btn-primary">Salvar Alterações</button>
            </div>
          </div>

          {/* Segurança */}
          <div className="glass-effect p-8 card-hover">
            <h2 className="text-2xl font-bold text-navy-900 mb-6 flex items-center gap-3">
              <Lock size={24} />
              Segurança
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Senha Atual</label>
                <input
                  type="password"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-navy-500 focus:border-transparent outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Nova Senha</label>
                <input
                  type="password"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-navy-500 focus:border-transparent outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Confirmar Senha</label>
                <input
                  type="password"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-navy-500 focus:border-transparent outline-none"
                />
              </div>
              <button className="btn-primary">Alterar Senha</button>
            </div>
          </div>

          {/* Notificações */}
          <div className="glass-effect p-8 card-hover">
            <h2 className="text-2xl font-bold text-navy-900 mb-6 flex items-center gap-3">
              <Bell size={24} />
              Notificações
            </h2>
            <div className="space-y-4">
              <label className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors">
                <input type="checkbox" defaultChecked className="w-5 h-5" />
                <span className="text-gray-700">Email de novos projetos</span>
              </label>
              <label className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors">
                <input type="checkbox" defaultChecked className="w-5 h-5" />
                <span className="text-gray-700">Alertas importantes</span>
              </label>
              <label className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors">
                <input type="checkbox" className="w-5 h-5" />
                <span className="text-gray-700">Newsletter semanal</span>
              </label>
              <button className="btn-primary">Salvar Preferências</button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
