import React, { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import { FileText, Search, Eye, Calendar, ChevronDown, Save, Sparkles, Loader, AlertCircle } from 'lucide-react';
import { api, Patient, NoteSummary } from '../services/api';

interface ClinicalNotesTabProps {
  darkMode: boolean;
}

// Template field configurations
const templateFields: Record<string, { label: string; placeholder: string; rows?: number }[]> = {
  'None': [],
  'Progress Note': [
    { label: 'Subjective', placeholder: 'Patient-reported symptoms and history...', rows: 4 },
    { label: 'Objective', placeholder: 'Physical examination findings, vital signs...', rows: 4 },
    { label: 'Assessment', placeholder: 'Clinical impression and diagnosis...', rows: 3 },
    { label: 'Plan', placeholder: 'Treatment plan and follow-up...', rows: 3 },
  ],
  'Admission Note': [
    { label: 'Reason for Admission', placeholder: 'Chief complaint and admission reason...', rows: 3 },
    { label: 'History of Present Illness', placeholder: 'Detailed history of current condition...', rows: 5 },
    { label: 'Past Medical History', placeholder: 'Relevant medical history...', rows: 3 },
    { label: 'Physical Examination', placeholder: 'Complete physical exam findings...', rows: 4 },
    { label: 'Initial Assessment & Plan', placeholder: 'Initial diagnostic impression and treatment plan...', rows: 4 },
  ],
  'Discharge Summary': [
    { label: 'Admission Date & Reason', placeholder: 'Date admitted and chief complaint...', rows: 2 },
    { label: 'Hospital Course', placeholder: 'Summary of treatment and hospital stay...', rows: 5 },
    { label: 'Discharge Diagnosis', placeholder: 'Final diagnosis at discharge...', rows: 2 },
    { label: 'Discharge Medications', placeholder: 'List of medications prescribed...', rows: 3 },
    { label: 'Follow-up Instructions', placeholder: 'Follow-up care and appointments...', rows: 3 },
  ],
  'Consultation': [
    { label: 'Reason for Consultation', placeholder: 'Why consultation was requested...', rows: 3 },
    { label: 'Review of Systems', placeholder: 'Relevant systems review...', rows: 4 },
    { label: 'Findings', placeholder: 'Consultation findings and observations...', rows: 4 },
    { label: 'Recommendations', placeholder: 'Specialist recommendations...', rows: 4 },
  ],
};

export function ClinicalNotesTab({ darkMode }: ClinicalNotesTabProps) {
  const [activeSubTab, setActiveSubTab] = useState<'compose' | 'library' | 'search'>('compose');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedTemplate, setSelectedTemplate] = useState('None');
  const [selectedPatientId, setSelectedPatientId] = useState<number | null>(null);
  const [visitDate, setVisitDate] = useState(new Date().toISOString().split('T')[0]);
  const [noteType, setNoteType] = useState('Progress Note');
  const [chiefComplaint, setChiefComplaint] = useState('');
  const [templateFieldValues, setTemplateFieldValues] = useState<Record<string, string>>({});

  // Data states
  const [patients, setPatients] = useState<Patient[]>([]);
  const [notes, setNotes] = useState<NoteSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const cardBgClass = darkMode
    ? 'bg-slate-800/80 border-slate-700/50'
    : 'bg-white/50 border-white/60';
  const textClass = darkMode ? 'text-white' : 'text-slate-900';
  const textSecondaryClass = darkMode ? 'text-slate-400' : 'text-slate-600';
  const inputBgClass = darkMode
    ? 'bg-slate-700/50 border-slate-600/40'
    : 'bg-white/50 border-white/40';

  const subTabs = [
    { id: 'compose' as const, label: 'Compose Note', icon: FileText },
    { id: 'library' as const, label: 'Notes Library', icon: FileText },
    { id: 'search' as const, label: 'Search', icon: Search },
  ];

  // Fetch patients on component mount
  useEffect(() => {
    fetchPatients();
    fetchNotes();
  }, []);

  // Refetch notes when switching to library or search tab
  useEffect(() => {
    if (activeSubTab === 'library' || activeSubTab === 'search') {
      fetchNotes();
    }
  }, [activeSubTab]);

  // Reset template fields when template changes
  useEffect(() => {
    const fields = templateFields[selectedTemplate] || [];
    const initialValues: Record<string, string> = {};
    fields.forEach(field => {
      initialValues[field.label] = '';
    });
    setTemplateFieldValues(initialValues);
  }, [selectedTemplate]);

  const fetchPatients = async () => {
    try {
      const data = await api.getPatients();
      setPatients(data);
      if (data.length > 0 && !selectedPatientId) {
        setSelectedPatientId(data[0].id);
      }
    } catch (error) {
      console.error('Failed to fetch patients:', error);
    }
  };

  const fetchNotes = async () => {
    try {
      setLoading(true);
      const data = await api.getNotes();
      // Sort notes by created_at in descending order (latest first)
      const sortedData = data.sort((a, b) => {
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
      });
      setNotes(sortedData);
      console.log('Fetched notes:', sortedData); // Debug log
    } catch (error: any) {
      console.error('Failed to fetch notes:', error);
      const errorMessage = error?.message || 'Failed to load notes';
      setMessage({ text: errorMessage, type: 'error' });
      setTimeout(() => setMessage(null), 5000);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveNote = async () => {
    if (!selectedPatientId) {
      setMessage({ text: 'Please select a patient', type: 'error' });
      return;
    }

    if (!chiefComplaint.trim() && Object.values(templateFieldValues).every(v => !v.trim())) {
      setMessage({ text: 'Please enter some content for the note', type: 'error' });
      return;
    }

    try {
      setSaving(true);

      // Build note content from template fields
      let content = '';
      if (chiefComplaint.trim()) {
        content += `**Chief Complaint:** ${chiefComplaint}\n\n`;
      }

      const fields = templateFields[selectedTemplate] || [];
      fields.forEach(field => {
        const value = templateFieldValues[field.label];
        if (value && value.trim()) {
          content += `**${field.label}:**\n${value}\n\n`;
        }
      });

      const noteData = {
        patient_id: selectedPatientId,
        title: `${noteType} - ${visitDate}`,
        content: content.trim() || 'No content provided',
        note_type: 'doctor_note', // Backend only accepts 'doctor_note' or 'nurse_note'
      };

      await api.createNote(noteData);

      setMessage({ text: 'Note saved successfully!', type: 'success' });

      // Reset form
      setChiefComplaint('');
      setTemplateFieldValues({});
      setSelectedTemplate('None');

      // Refresh notes list
      await fetchNotes();

      // Clear message after 3 seconds
      setTimeout(() => setMessage(null), 3000);
    } catch (error: any) {
      console.error('Error saving note:', error);
      const errorMessage = error?.message || error?.toString() || 'Failed to save note';
      setMessage({ text: errorMessage, type: 'error' });
      setTimeout(() => setMessage(null), 5000);
    } finally {
      setSaving(false);
    }
  };

  const handleGenerateWithAI = async () => {
    setMessage({ text: 'AI generation is not yet implemented. Use "Save Note" to save your content.', type: 'error' });
    setTimeout(() => setMessage(null), 3000);
  };

  const filteredNotes = notes.filter(note => {
    if (!searchTerm) return true;
    const searchLower = searchTerm.toLowerCase();
    return (
      note.title.toLowerCase().includes(searchLower) ||
      (note.summary && note.summary.toLowerCase().includes(searchLower)) ||
      note.note_type.toLowerCase().includes(searchLower) ||
      note.patient_name.toLowerCase().includes(searchLower) ||
      note.author_name.toLowerCase().includes(searchLower)
    );
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className={`text-xl ${textClass} mb-1`}>Clinical Documentation Studio</h2>
        <p className={textSecondaryClass}>Create structured notes, review prior encounters, and search your documentation.</p>
      </div>

      {/* Sub Tabs */}
      <div className={`inline-flex gap-2 p-1.5 ${cardBgClass} backdrop-blur-xl rounded-2xl border shadow-lg`}>
        {subTabs.map((tab) => (
          <motion.button
            key={tab.id}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setActiveSubTab(tab.id)}
            className={`relative flex items-center gap-2 px-4 py-2 rounded-xl transition-all ${
              activeSubTab === tab.id
                ? darkMode
                  ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white'
                  : 'bg-gradient-to-r from-purple-500 to-indigo-500 text-white'
                : darkMode
                ? 'text-slate-400 hover:text-white'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            <span className="text-sm">{tab.label}</span>
          </motion.button>
        ))}
      </div>

      {/* Message Display */}
      {message && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          className={`p-4 rounded-xl border flex items-center gap-3 ${
            message.type === 'success'
              ? 'bg-green-500/10 border-green-500/40 text-green-400'
              : 'bg-red-500/10 border-red-500/40 text-red-400'
          }`}
        >
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{message.text}</span>
        </motion.div>
      )}

      {/* Compose Note Content */}
      {activeSubTab === 'compose' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-8 border shadow-lg`}
        >
          <div className="space-y-6">
            {/* Select Template Section */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className={`${textClass}`}>Select Template</h3>
              </div>

              {/* Note Templates Library */}
              <div className="mb-6 p-4 bg-gradient-to-r from-purple-500/10 to-indigo-500/10 rounded-xl border border-purple-500/20">
                <div className="flex items-center gap-2 mb-3">
                  <FileText className="w-5 h-5 text-purple-500" />
                  <h4 className={`${textClass}`}>Note Templates Library</h4>
                </div>

                {/* Filter by Category */}
                <div className="mb-4">
                  <label className={`block text-sm ${textSecondaryClass} mb-2`}>Filter by Category</label>
                  <div className="relative">
                    <select
                      value={selectedCategory}
                      onChange={(e) => setSelectedCategory(e.target.value)}
                      className={`w-full px-4 py-2.5 ${inputBgClass} backdrop-blur-sm border rounded-xl ${textClass} appearance-none focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all cursor-pointer`}
                    >
                      <option>All</option>
                      <option>Cardiology</option>
                      <option>Neurology</option>
                      <option>Pediatrics</option>
                      <option>Emergency</option>
                    </select>
                    <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
                  </div>
                </div>

                {/* Select Template */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className={`text-sm ${textSecondaryClass}`}>Select Template</label>
                  </div>
                  <div className="relative">
                    <select
                      value={selectedTemplate}
                      onChange={(e) => setSelectedTemplate(e.target.value)}
                      className={`w-full px-4 py-2.5 ${inputBgClass} backdrop-blur-sm border rounded-xl ${textClass} appearance-none focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all cursor-pointer`}
                    >
                      <option>None</option>
                      <option>Progress Note</option>
                      <option>Admission Note</option>
                      <option>Discharge Summary</option>
                      <option>Consultation</option>
                    </select>
                    <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
                  </div>
                </div>
              </div>

              {/* Patient and Visit Info Grid */}
              <div className="grid md:grid-cols-2 gap-4 mb-6">
                {/* Patient */}
                <div>
                  <label className={`block text-sm ${textSecondaryClass} mb-2`}>Patient</label>
                  <div className="relative">
                    <select
                      value={selectedPatientId || ''}
                      onChange={(e) => setSelectedPatientId(Number(e.target.value))}
                      className={`w-full px-4 py-2.5 ${inputBgClass} backdrop-blur-sm border rounded-xl ${textClass} appearance-none focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all cursor-pointer`}
                    >
                      {patients.map(patient => (
                        <option key={patient.id} value={patient.id}>
                          {patient.first_name} {patient.last_name} (#{patient.id})
                        </option>
                      ))}
                    </select>
                    <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
                  </div>
                </div>

                {/* Visit Date */}
                <div>
                  <label className={`block text-sm ${textSecondaryClass} mb-2`}>Visit Date</label>
                  <div className="relative">
                    <Calendar className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="date"
                      value={visitDate}
                      onChange={(e) => setVisitDate(e.target.value)}
                      className={`w-full pl-11 pr-4 py-2.5 ${inputBgClass} backdrop-blur-sm border rounded-xl ${textClass} focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all`}
                    />
                  </div>
                </div>
              </div>

              {/* Note Type and Chief Complaint */}
              <div className="grid md:grid-cols-2 gap-4 mb-6">
                {/* Note Type */}
                <div>
                  <label className={`block text-sm ${textSecondaryClass} mb-2`}>Note Type</label>
                  <div className="relative">
                    <select
                      value={noteType}
                      onChange={(e) => setNoteType(e.target.value)}
                      className={`w-full px-4 py-2.5 ${inputBgClass} backdrop-blur-sm border rounded-xl ${textClass} appearance-none focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all cursor-pointer`}
                    >
                      <option>Progress Note</option>
                      <option>Initial Assessment</option>
                      <option>Follow-up</option>
                      <option>Procedure Note</option>
                    </select>
                    <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
                  </div>
                </div>

                {/* Chief Complaint */}
                <div>
                  <label className={`block text-sm ${textSecondaryClass} mb-2`}>Chief Complaint</label>
                  <input
                    type="text"
                    value={chiefComplaint}
                    onChange={(e) => setChiefComplaint(e.target.value)}
                    placeholder="Enter chief complaint"
                    className={`w-full px-4 py-2.5 ${inputBgClass} backdrop-blur-sm border rounded-xl ${textClass} placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all`}
                  />
                </div>
              </div>

              {/* Template-based Structured Fields */}
              {selectedTemplate !== 'None' && (
                <div>
                  <h4 className={`${textClass} mb-4`}>Structured Fields ({selectedTemplate})</h4>

                  <div className="space-y-4">
                    {templateFields[selectedTemplate]?.map((field) => (
                      <div key={field.label}>
                        <label className={`block text-sm ${textSecondaryClass} mb-2`}>{field.label}</label>
                        <textarea
                          value={templateFieldValues[field.label] || ''}
                          onChange={(e) => setTemplateFieldValues({
                            ...templateFieldValues,
                            [field.label]: e.target.value
                          })}
                          placeholder={field.placeholder}
                          rows={field.rows || 4}
                          className={`w-full px-4 py-3 ${inputBgClass} backdrop-blur-sm border rounded-xl ${textClass} placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all resize-none`}
                        />
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex gap-3 pt-4">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleSaveNote}
                  disabled={saving}
                  className="flex-1 px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  {saving ? (
                    <>
                      <Loader className="w-5 h-5 animate-spin" />
                      <span className="font-semibold">Saving...</span>
                    </>
                  ) : (
                    <>
                      <Save className="w-5 h-5" />
                      <span className="font-semibold">Save Note</span>
                    </>
                  )}
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleGenerateWithAI}
                  className={`px-6 py-3 ${
                    darkMode ? 'bg-slate-700 text-slate-300 hover:bg-slate-600' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  } rounded-xl transition-colors flex items-center gap-2`}
                >
                  <Sparkles className="w-5 h-5" />
                  <span>Generate with AI</span>
                </motion.button>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Library Tab */}
      {activeSubTab === 'library' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="space-y-4"
        >
          {loading ? (
            <div className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-12 border shadow-lg text-center`}>
              <Loader className="w-12 h-12 mx-auto mb-4 text-purple-500 animate-spin" />
              <p className={textSecondaryClass}>Loading notes...</p>
            </div>
          ) : notes.length === 0 ? (
            <div className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-12 border shadow-lg text-center`}>
              <FileText className="w-16 h-16 mx-auto mb-4 text-purple-500" />
              <h3 className={`text-xl ${textClass} mb-2`}>No Notes Yet</h3>
              <p className={textSecondaryClass}>Create your first clinical note using the Compose tab</p>
            </div>
          ) : (
            <>
              <div className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-6 border shadow-lg`}>
                <h3 className={`text-lg ${textClass} mb-1`}>Notes Library</h3>
                <p className={`text-sm ${textSecondaryClass} mb-4`}>
                  {notes.length} clinical {notes.length === 1 ? 'note' : 'notes'} available
                </p>
              </div>

              {notes.map((note) => {
                return (
                  <motion.div
                    key={note.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-6 border shadow-lg hover:border-purple-500/50 transition-all cursor-pointer`}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <h4 className={`${textClass} mb-1`}>{note.title}</h4>
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className={`text-sm ${textSecondaryClass}`}>
                            Patient: {note.patient_name}
                          </span>
                          <span className="text-purple-400">•</span>
                          <span className={`text-sm ${textSecondaryClass}`}>
                            By: {note.author_name}
                          </span>
                          <span className="text-purple-400">•</span>
                          <span className={`text-sm ${textSecondaryClass}`}>
                            {new Date(note.created_at).toLocaleDateString('en-US', {
                              month: 'short',
                              day: 'numeric',
                              year: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {note.risk_level && (
                          <span className={`px-3 py-1 rounded-full text-xs ${
                            note.risk_level === 'high'
                              ? 'bg-red-500/20 text-red-400 border border-red-500/40'
                              : note.risk_level === 'medium'
                              ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/40'
                              : 'bg-green-500/20 text-green-400 border border-green-500/40'
                          }`}>
                            {note.risk_level}
                          </span>
                        )}
                      </div>
                    </div>
                    {note.summary && (
                      <p className={`text-sm ${textSecondaryClass} line-clamp-3`}>
                        {note.summary}
                      </p>
                    )}
                  </motion.div>
                );
              })}
            </>
          )}
        </motion.div>
      )}

      {/* Search Tab */}
      {activeSubTab === 'search' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="space-y-4"
        >
          <div className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-6 border shadow-lg`}>
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search notes by title, content, or type..."
                className={`w-full pl-12 pr-4 py-3 ${inputBgClass} backdrop-blur-sm border rounded-xl ${textClass} placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all`}
              />
            </div>
          </div>

          {filteredNotes.length === 0 ? (
            <div className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-12 border shadow-lg text-center`}>
              <Search className="w-16 h-16 mx-auto mb-4 text-purple-500" />
              <h3 className={`text-xl ${textClass} mb-2`}>No Results Found</h3>
              <p className={textSecondaryClass}>
                {searchTerm ? 'Try different search terms' : 'Enter a search term to find notes'}
              </p>
            </div>
          ) : (
            <>
              <div className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-4 border shadow-lg`}>
                <p className={`text-sm ${textSecondaryClass}`}>
                  Found {filteredNotes.length} {filteredNotes.length === 1 ? 'result' : 'results'}
                </p>
              </div>

              {filteredNotes.map((note) => {
                return (
                  <motion.div
                    key={note.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`${cardBgClass} backdrop-blur-xl rounded-2xl p-6 border shadow-lg hover:border-purple-500/50 transition-all cursor-pointer`}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <h4 className={`${textClass} mb-1`}>{note.title}</h4>
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className={`text-sm ${textSecondaryClass}`}>
                            Patient: {note.patient_name}
                          </span>
                          <span className="text-purple-400">•</span>
                          <span className={`text-sm ${textSecondaryClass}`}>
                            By: {note.author_name}
                          </span>
                          <span className="text-purple-400">•</span>
                          <span className={`text-sm ${textSecondaryClass}`}>
                            {new Date(note.created_at).toLocaleDateString('en-US', {
                              month: 'short',
                              day: 'numeric',
                              year: 'numeric',
                            })}
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {note.risk_level && (
                          <span className={`px-3 py-1 rounded-full text-xs ${
                            note.risk_level === 'high'
                              ? 'bg-red-500/20 text-red-400 border border-red-500/40'
                              : note.risk_level === 'medium'
                              ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/40'
                              : 'bg-green-500/20 text-green-400 border border-green-500/40'
                          }`}>
                            {note.risk_level}
                          </span>
                        )}
                      </div>
                    </div>
                    {note.summary && (
                      <p className={`text-sm ${textSecondaryClass} line-clamp-2`}>
                        {note.summary}
                      </p>
                    )}
                  </motion.div>
                );
              })}
            </>
          )}
        </motion.div>
      )}
    </div>
  );
}
