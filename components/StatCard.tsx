'use client'

import { TrendingUp, AlertCircle, CheckCircle, Clock } from 'lucide-react'

interface StatCardProps {
  title: string
  value: string | number
  change?: string
  icon: React.ReactNode
  color: 'navy' | 'teal' | 'amber' | 'red'
}

const colorClasses = {
  navy: 'bg-navy-50 text-navy-700',
  teal: 'bg-teal-50 text-teal-700',
  amber: 'bg-amber-50 text-amber-700',
  red: 'bg-red-50 text-red-700',
}

const iconBgClasses = {
  navy: 'bg-navy-100',
  teal: 'bg-teal-100',
  amber: 'bg-amber-100',
  red: 'bg-red-100',
}

export function StatCard({ title, value, change, icon, color }: StatCardProps) {
  return (
    <div className={`card-hover rounded-xl p-6 ${colorClasses[color]} border border-transparent hover:border-gray-200`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium opacity-75">{title}</p>
          <h3 className="text-3xl font-bold mt-2">{value}</h3>
          {change && (
            <p className="text-sm mt-2 flex items-center gap-1">
              <TrendingUp size={16} />
              {change}
            </p>
          )}
        </div>
        <div className={`w-14 h-14 rounded-xl flex items-center justify-center text-2xl ${iconBgClasses[color]}`}>
          {icon}
        </div>
      </div>
    </div>
  )
}

export function StatsGrid() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatCard
        title="Projetos Ativos"
        value="24"
        change="+12% este mês"
        icon="📊"
        color="navy"
      />
      <StatCard
        title="Concluídos"
        value="156"
        change="+8% este mês"
        icon={<CheckCircle size={32} />}
        color="teal"
      />
      <StatCard
        title="Em Andamento"
        value="48"
        change="+3% este mês"
        icon={<Clock size={32} />}
        color="amber"
      />
      <StatCard
        title="Alertas"
        value="5"
        change="-2% este mês"
        icon={<AlertCircle size={32} />}
        color="red"
      />
    </div>
  )
}
