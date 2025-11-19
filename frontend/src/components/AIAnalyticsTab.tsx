import React, { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import {
  Brain,
  Users,
  FileText,
  Calendar as CalendarIcon,
  AlertTriangle,
  Clock,
  TrendingUp,
  Activity,
  Loader,
  CheckCircle2,
  AlertCircle,
  Plus,
} from 'lucide-react';
import { api, Patient, Note, Appointment } from '../services/api';

interface Task {
  id: string;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  dueDate: string;
  dueTime: string;
  status: 'pending' | 'completed';
  createdAt: string;
  completedAt?: string;
}

interface AIAnalyticsTabProps {
  darkMode: boolean;
  tasks: Task[];
  setActiveTab: (tab: 'dashboard' | 'patients' | 'notes' | 'tasks' | 'analytics' | 'calendar') => void;
}

export function AIAnalyticsTab({ darkMode, tasks, setActiveTab }: AIAnalyticsTabProps) {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [notes, setNotes] = useState<Note[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);

  const cardBgClass = darkMode
    ? 'bg-slate-800/80 border-slate-700/50'
    : 'bg-white/50 border-white/60';
  const textClass = darkMode ? 'text-white' : 'text-slate-900';
  const textSecondaryClass = darkMode ? 'text-slate-400' : 'text-slate-600';

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      const [patientsData, notesData, appointmentsData] = await Promise.all([
        api.getPatients(),
        api.getNotes(),
        api.getAppointments(),
      ]);
      setPatients(patientsData);
      setNotes(notesData);
      setAppointments(appointmentsData);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Calculate insights
  const totalPatients = patients.length;
  const recentNotes = notes.slice(0, 5);
  const upcomingAppointments = appointments
    .filter(apt => new Date(apt.start_time) > new Date())
    .sort((a, b) => new Date(a.start_time).getTime() - new Date(b.start_time).getTime())
    .slice(0, 5);

  const todayAppointments = appointments.filter(apt => {
    const aptDate = new Date(apt.start_time);
    const today = new Date();
    return (
      aptDate.getDate() === today.getDate() &&
      aptDate.getMonth() === today.getMonth() &&
      aptDate.getFullYear() === today.getFullYear()
    );
  });

  const pendingTasks = tasks.filter(task => task.status === 'pending').length;

  const stats = [
    {
      icon: Users,
      label: 'Total Patients',
      value: totalPatients.toString(),
      change: 'Active in system',
      gradient: 'from-blue-500 to-cyan-500',
    },
    {
      icon: FileText,
      label: 'Clinical Notes',
      value: notes.length.toString(),
      change: `${recentNotes.length} recent`,
      gradient: 'from-purple-500 to-indigo-500',
    },
    {
      icon: CalendarIcon,
      label: 'Appointments Today',
      value: todayAppointments.length.toString(),
      change: `${upcomingAppointments.length} upcoming`,
      gradient: 'from-green-500 to-emerald-500',
    },
    {
      icon: Clock,
      label: 'Pending Tasks',
      value: pendingTasks.toString(),
      change: 'Requires attention',
      gradient: 'from-orange-500 to-red-500',
    },
  ];

  if (loading) {
    return (
      <div className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-12 border shadow-lg text-center`}>
        <Loader className="w-12 h-12 mx-auto mb-4 text-purple-500 animate-spin" />
        <p className={textSecondaryClass}>Loading analytics...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className={`text-xl ${textClass} mb-1`}>AI & Analytics Dashboard</h2>
        <p className={textSecondaryClass}>
          Comprehensive overview of patient care, clinical documentation, and upcoming tasks
        </p>
      </div>

      {/* Main Layout: Summary on Left, Todo on Right */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Column - Summary (2/3 width) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Stats Grid */}
          <div className="grid grid-cols-2 gap-4">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1, duration: 0.4 }}
                whileHover={{ y: -4 }}
                className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-6 border shadow-lg hover:shadow-xl transition-all`}
              >
                <div className="flex items-center justify-between mb-4">
                  <div className={`p-3 bg-gradient-to-br ${stat.gradient} rounded-xl shadow-lg`}>
                    <stat.icon className="w-6 h-6 text-white" />
                  </div>
                </div>
                <h3 className={`text-3xl mb-2 ${textClass}`}>{stat.value}</h3>
                <p className={`text-sm ${textSecondaryClass} mb-1`}>{stat.label}</p>
                <p className="text-xs text-green-500">{stat.change}</p>
              </motion.div>
            ))}
          </div>

          {/* Recent Activity Summary */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-6 border shadow-lg`}
          >
            <div className="flex items-center gap-2 mb-4">
              <Activity className="w-5 h-5 text-purple-500" />
              <h3 className={`text-lg ${textClass}`}>Recent Activity Summary</h3>
            </div>

            <div className="space-y-4">
              {/* Patients Summary */}
              <div className={`p-4 ${darkMode ? 'bg-slate-700/50' : 'bg-white/60'} rounded-xl border ${
                darkMode ? 'border-slate-600' : 'border-white/40'
              }`}>
                <div className="flex items-center gap-3 mb-2">
                  <Users className="w-5 h-5 text-blue-400" />
                  <h4 className={`${textClass} font-semibold`}>Patients</h4>
                </div>
                <p className={`text-sm ${textSecondaryClass}`}>
                  {totalPatients} total patients in system
                  {patients.length > 0 && ` • Latest: ${patients[0].first_name} ${patients[0].last_name}`}
                </p>
              </div>

              {/* Notes Summary */}
              <div className={`p-4 ${darkMode ? 'bg-slate-700/50' : 'bg-white/60'} rounded-xl border ${
                darkMode ? 'border-slate-600' : 'border-white/40'
              }`}>
                <div className="flex items-center gap-3 mb-2">
                  <FileText className="w-5 h-5 text-purple-400" />
                  <h4 className={`${textClass} font-semibold`}>Clinical Notes</h4>
                </div>
                <p className={`text-sm ${textSecondaryClass}`}>
                  {notes.length} total notes • {recentNotes.length} created recently
                  {notes.length > 0 && ` • Latest: ${notes[0].title}`}
                </p>
              </div>

              {/* Appointments Summary */}
              <div className={`p-4 ${darkMode ? 'bg-slate-700/50' : 'bg-white/60'} rounded-xl border ${
                darkMode ? 'border-slate-600' : 'border-white/40'
              }`}>
                <div className="flex items-center gap-3 mb-2">
                  <CalendarIcon className="w-5 h-5 text-green-400" />
                  <h4 className={`${textClass} font-semibold`}>Appointments</h4>
                </div>
                <p className={`text-sm ${textSecondaryClass}`}>
                  {todayAppointments.length} appointments today • {upcomingAppointments.length} upcoming
                </p>
              </div>

              {/* Tasks Summary */}
              <div className={`p-4 ${darkMode ? 'bg-slate-700/50' : 'bg-white/60'} rounded-xl border ${
                darkMode ? 'border-slate-600' : 'border-white/40'
              }`}>
                <div className="flex items-center gap-3 mb-2">
                  <CheckCircle2 className="w-5 h-5 text-orange-400" />
                  <h4 className={`${textClass} font-semibold`}>Tasks</h4>
                </div>
                <p className={`text-sm ${textSecondaryClass}`}>
                  {pendingTasks} pending tasks • {tasks.filter(t => t.status === 'completed').length} completed
                </p>
              </div>
            </div>
          </motion.div>

          {/* AI Insights */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-6 border shadow-lg`}
          >
            <div className="flex items-center gap-2 mb-4">
              <Brain className="w-5 h-5 text-purple-500" />
              <h3 className={`text-lg ${textClass}`}>AI-Powered Insights</h3>
            </div>

            <div className="grid md:grid-cols-3 gap-4">
              <div className={`p-4 ${darkMode ? 'bg-slate-700/50' : 'bg-white/60'} rounded-xl border ${
                darkMode ? 'border-slate-600' : 'border-white/40'
              }`}>
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="w-4 h-4 text-green-400" />
                  <h4 className={`text-sm ${textClass} font-semibold`}>Clinical Efficiency</h4>
                </div>
                <p className="text-2xl font-bold text-green-400 mb-1">86%</p>
                <p className={`text-xs ${textSecondaryClass}`}>
                  Documentation completion rate
                </p>
              </div>

              <div className={`p-4 ${darkMode ? 'bg-slate-700/50' : 'bg-white/60'} rounded-xl border ${
                darkMode ? 'border-slate-600' : 'border-white/40'
              }`}>
                <div className="flex items-center gap-2 mb-2">
                  <Activity className="w-4 h-4 text-blue-400" />
                  <h4 className={`text-sm ${textClass} font-semibold`}>Patient Load</h4>
                </div>
                <p className="text-2xl font-bold text-blue-400 mb-1">{totalPatients}</p>
                <p className={`text-xs ${textSecondaryClass}`}>
                  Active patients under care
                </p>
              </div>

              <div className={`p-4 ${darkMode ? 'bg-slate-700/50' : 'bg-white/60'} rounded-xl border ${
                darkMode ? 'border-slate-600' : 'border-white/40'
              }`}>
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle2 className="w-4 h-4 text-purple-400" />
                  <h4 className={`text-sm ${textClass} font-semibold`}>Task Completion</h4>
                </div>
                <p className="text-2xl font-bold text-purple-400 mb-1">
                  {tasks.filter(t => t.status === 'completed').length}
                </p>
                <p className={`text-xs ${textSecondaryClass}`}>
                  Completed tasks
                </p>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Right Column - Quick Todo List (1/3 width) */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-6 border shadow-lg h-fit sticky top-6`}
        >
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-purple-500" />
              <h3 className={`text-lg ${textClass}`}>Quick Todo</h3>
            </div>
            <span className={`text-xs ${textSecondaryClass}`}>
              {tasks.filter(t => t.status === 'pending').length} pending
            </span>
          </div>

          <div className="space-y-3">
            {tasks.filter(t => t.status === 'pending').length === 0 ? (
              <div className="text-center py-8">
                <CheckCircle2 className="w-12 h-12 mx-auto mb-3 text-green-500 opacity-50" />
                <p className={textSecondaryClass}>No pending tasks</p>
              </div>
            ) : (
              tasks.filter(t => t.status === 'pending').slice(0, 5).map((task) => {
                const isOverdue = new Date(`${task.dueDate}T${task.dueTime}`) < new Date();
                const dueDateTime = new Date(`${task.dueDate}T${task.dueTime}`);
                const isToday = dueDateTime.toDateString() === new Date().toDateString();

                return (
                  <div
                    key={task.id}
                    className={`p-3 ${darkMode ? 'bg-slate-700/50' : 'bg-white/60'} rounded-xl border ${
                      isOverdue
                        ? 'border-red-500/50'
                        : darkMode
                        ? 'border-slate-600'
                        : 'border-white/40'
                    } hover:border-purple-500/50 transition-all cursor-pointer`}
                    onClick={() => setActiveTab('tasks')}
                  >
                    <div className="flex items-start gap-2">
                      <div className="flex-1 min-w-0">
                        <p className={`text-sm ${textClass} mb-1 line-clamp-1`}>{task.title}</p>
                        <div className="flex items-center gap-2 flex-wrap">
                          <p className={`text-xs ${isOverdue ? 'text-red-400' : textSecondaryClass} flex items-center gap-1`}>
                            <Clock className="w-3 h-3" />
                            {isToday ? task.dueTime : dueDateTime.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} {isToday && task.dueTime}
                          </p>
                          {isOverdue && (
                            <span className="text-xs text-red-400 flex items-center gap-1">
                              <AlertCircle className="w-3 h-3" />
                              Overdue
                            </span>
                          )}
                        </div>
                        {task.priority === 'high' && (
                          <span className="inline-block mt-1 px-2 py-0.5 rounded-full text-xs bg-red-500/20 text-red-400 border border-red-500/40">
                            High Priority
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })
            )}

            <button
              onClick={() => setActiveTab('tasks')}
              className={`w-full p-3 border border-dashed ${
                darkMode ? 'border-slate-600 hover:border-purple-500/50' : 'border-slate-300 hover:border-purple-500/50'
              } rounded-xl transition-colors flex items-center justify-center gap-2 ${textSecondaryClass} hover:text-purple-500`}
            >
              <Plus className="w-4 h-4" />
              <span className="text-sm">Add task</span>
            </button>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-700/50">
            <button
              onClick={() => setActiveTab('tasks')}
              className="w-full px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl shadow-lg hover:shadow-xl transition-all text-sm font-semibold"
            >
              View All Tasks
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
