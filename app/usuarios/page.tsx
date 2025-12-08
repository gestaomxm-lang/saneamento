import Navbar from '@/components/Navbar'
import { Trash2, Edit2, CheckCircle, Clock } from 'lucide-react'

const usuarios = [
  { id: 1, nome: 'João Silva', email: 'joao@example.com', cargo: 'Gerente', status: 'Ativo' },
  { id: 2, nome: 'Maria Santos', email: 'maria@example.com', cargo: 'Analista', status: 'Ativo' },
  { id: 3, nome: 'Pedro Costa', email: 'pedro@example.com', cargo: 'Desenvolvedor', status: 'Inativo' },
  { id: 4, nome: 'Ana Paula', email: 'ana@example.com', cargo: 'Designer', status: 'Ativo' },
  { id: 5, nome: 'Carlos Oliveira', email: 'carlos@example.com', cargo: 'Gerente', status: 'Ativo' },
]

export default function Usuarios() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
      <Navbar />

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold gradient-text">Usuários</h1>
          <button className="btn-primary">+ Novo Usuário</button>
        </div>

        <div className="glass-effect overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-navy-50 border-b border-gray-200">
                  <th className="px-6 py-4 text-left text-sm font-semibold text-navy-900">Nome</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-navy-900">Email</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-navy-900">Cargo</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-navy-900">Status</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-navy-900">Ações</th>
                </tr>
              </thead>
              <tbody>
                {usuarios.map((user, idx) => (
                  <tr key={user.id} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-6 py-4 font-medium text-gray-900">{user.nome}</td>
                    <td className="px-6 py-4 text-gray-600">{user.email}</td>
                    <td className="px-6 py-4 text-gray-600">{user.cargo}</td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${
                        user.status === 'Ativo'
                          ? 'bg-teal-100 text-teal-700'
                          : 'bg-gray-100 text-gray-700'
                      }`}>
                        {user.status === 'Ativo' ? <CheckCircle size={16} /> : <Clock size={16} />}
                        {user.status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex gap-2">
                        <button className="p-2 hover:bg-navy-100 rounded-lg transition-colors text-navy-600">
                          <Edit2 size={18} />
                        </button>
                        <button className="p-2 hover:bg-red-100 rounded-lg transition-colors text-red-600">
                          <Trash2 size={18} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  )
}
