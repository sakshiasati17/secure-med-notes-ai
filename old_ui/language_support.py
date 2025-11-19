"""
Multi-language Support System
Supports: English, Spanish, French, German, Hindi, Chinese
"""
import streamlit as st

# Language translations
TRANSLATIONS = {
    "en": {
        "name": "English",
        "flag": "🇺🇸",
        "app_title": "Secure Medical Notes AI",
        "login": "Login",
        "logout": "Logout",
        "email": "Email",
        "password": "Password",
        "doctor_notes": "Doctor Notes",
        "nurse_notes": "Nurse Notes",
        "ai_dashboard": "AI Dashboard",
        "calendar": "Calendar",
        "summaries": "Summaries",
        "risk_reports": "Risk Reports",
        "notifications": "Notifications",
        "audit_trail": "Audit Trail",
        "patient_id": "Patient ID",
        "note_title": "Note Title",
        "note_content": "Note Content",
        "create_note": "Create Note",
        "recent_notes": "Recent Notes",
        "welcome_message": "Welcome to Secure Medical Notes AI",
        "ai_services": "AI Services",
        "operational": "Operational",
        "not_available": "Not Available"
    },
    
    "es": {
        "name": "Español",
        "flag": "🇪🇸",
        "app_title": "Notas Médicas Seguras IA",
        "login": "Iniciar Sesión",
        "logout": "Cerrar Sesión",
        "email": "Correo Electrónico",
        "password": "Contraseña",
        "doctor_notes": "Notas del Doctor",
        "nurse_notes": "Notas de Enfermería",
        "ai_dashboard": "Panel de IA",
        "calendar": "Calendario",
        "summaries": "Resúmenes",
        "risk_reports": "Informes de Riesgo",
        "notifications": "Notificaciones",
        "audit_trail": "Registro de Auditoría",
        "patient_id": "ID del Paciente",
        "note_title": "Título de la Nota",
        "note_content": "Contenido de la Nota",
        "create_note": "Crear Nota",
        "recent_notes": "Notas Recientes",
        "welcome_message": "Bienvenido a Notas Médicas Seguras IA",
        "ai_services": "Servicios de IA",
        "operational": "Operativo",
        "not_available": "No Disponible"
    },
    
    "fr": {
        "name": "Français",
        "flag": "🇫🇷",
        "app_title": "Notes Médicales Sécurisées IA",
        "login": "Connexion",
        "logout": "Déconnexion",
        "email": "E-mail",
        "password": "Mot de Passe",
        "doctor_notes": "Notes du Médecin",
        "nurse_notes": "Notes d'Infirmière",
        "ai_dashboard": "Tableau de Bord IA",
        "calendar": "Calendrier",
        "summaries": "Résumés",
        "risk_reports": "Rapports de Risque",
        "notifications": "Notifications",
        "audit_trail": "Journal d'Audit",
        "patient_id": "ID Patient",
        "note_title": "Titre de la Note",
        "note_content": "Contenu de la Note",
        "create_note": "Créer une Note",
        "recent_notes": "Notes Récentes",
        "welcome_message": "Bienvenue dans Notes Médicales Sécurisées IA",
        "ai_services": "Services IA",
        "operational": "Opérationnel",
        "not_available": "Non Disponible"
    },
    
    "de": {
        "name": "Deutsch",
        "flag": "🇩🇪",
        "app_title": "Sichere Medizinische Notizen KI",
        "login": "Anmelden",
        "logout": "Abmelden",
        "email": "E-Mail",
        "password": "Passwort",
        "doctor_notes": "Arztnotizen",
        "nurse_notes": "Krankenpflegernotizen",
        "ai_dashboard": "KI-Dashboard",
        "calendar": "Kalender",
        "summaries": "Zusammenfassungen",
        "risk_reports": "Risikoberichte",
        "notifications": "Benachrichtigungen",
        "audit_trail": "Prüfpfad",
        "patient_id": "Patienten-ID",
        "note_title": "Notiz Titel",
        "note_content": "Notiz Inhalt",
        "create_note": "Notiz Erstellen",
        "recent_notes": "Letzte Notizen",
        "welcome_message": "Willkommen bei Sichere Medizinische Notizen KI",
        "ai_services": "KI-Dienste",
        "operational": "Betriebsbereit",
        "not_available": "Nicht Verfügbar"
    },
    
    "hi": {
        "name": "हिन्दी",
        "flag": "🇮🇳",
        "app_title": "सुरक्षित चिकित्सा नोट्स एआई",
        "login": "लॉगिन",
        "logout": "लॉगआउट",
        "email": "ईमेल",
        "password": "पासवर्ड",
        "doctor_notes": "डॉक्टर के नोट्स",
        "nurse_notes": "नर्स के नोट्स",
        "ai_dashboard": "एआई डैशबोर्ड",
        "calendar": "कैलेंडर",
        "summaries": "सारांश",
        "risk_reports": "जोखिम रिपोर्ट",
        "notifications": "सूचनाएं",
        "audit_trail": "ऑडिट ट्रेल",
        "patient_id": "रोगी आईडी",
        "note_title": "नोट शीर्षक",
        "note_content": "नोट सामग्री",
        "create_note": "नोट बनाएं",
        "recent_notes": "हाल के नोट्स",
        "welcome_message": "सुरक्षित चिकित्सा नोट्स एआई में आपका स्वागत है",
        "ai_services": "एआई सेवाएं",
        "operational": "परिचालन",
        "not_available": "उपलब्ध नहीं"
    },
    
    "zh": {
        "name": "中文",
        "flag": "🇨🇳",
        "app_title": "安全医疗笔记人工智能",
        "login": "登录",
        "logout": "登出",
        "email": "电子邮件",
        "password": "密码",
        "doctor_notes": "医生笔记",
        "nurse_notes": "护士笔记",
        "ai_dashboard": "人工智能仪表板",
        "calendar": "日历",
        "summaries": "摘要",
        "risk_reports": "风险报告",
        "notifications": "通知",
        "audit_trail": "审计追踪",
        "patient_id": "患者编号",
        "note_title": "笔记标题",
        "note_content": "笔记内容",
        "create_note": "创建笔记",
        "recent_notes": "最近的笔记",
        "welcome_message": "欢迎使用安全医疗笔记人工智能",
        "ai_services": "人工智能服务",
        "operational": "运营中",
        "not_available": "不可用"
    }
}

def init_language():
    """Initialize language in session state"""
    if 'language' not in st.session_state:
        st.session_state.language = 'en'

def set_language(lang_code):
    """Set the current language"""
    st.session_state.language = lang_code

def get_text(key):
    """Get translated text for the current language"""
    lang = st.session_state.get('language', 'en')
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

def show_language_selector():
    """Display language selector in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🌐 Language / Idioma")
    
    current_lang = st.session_state.get('language', 'en')
    
    # Create language options with flags
    lang_options = {
        code: f"{data['flag']} {data['name']}" 
        for code, data in TRANSLATIONS.items()
    }
    
    # Find current selection
    current_selection = lang_options.get(current_lang, lang_options['en'])
    
    # Language selector
    selected = st.sidebar.selectbox(
        "Select Language",
        options=list(lang_options.values()),
        index=list(lang_options.values()).index(current_selection),
        label_visibility="collapsed"
    )
    
    # Find language code from selection
    selected_code = [code for code, label in lang_options.items() if label == selected][0]
    
    # Update language if changed
    if selected_code != current_lang:
        set_language(selected_code)
        st.rerun()

def translate_note_content(text: str, target_lang: str) -> str:
    """
    Translate note content using AI
    This is a placeholder - in production, integrate with Google Translate API or OpenAI
    """
    # Mock translation - replace with actual API call
    if target_lang == 'es':
        return f"[Traducido al español] {text}"
    elif target_lang == 'fr':
        return f"[Traduit en français] {text}"
    elif target_lang == 'de':
        return f"[Übersetzt ins Deutsche] {text}"
    elif target_lang == 'hi':
        return f"[हिंदी में अनुवादित] {text}"
    elif target_lang == 'zh':
        return f"[翻译成中文] {text}"
    else:
        return text

def show_translation_feature(text: str):
    """Show translation feature for note content"""
    st.write("**Translate This Note:**")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        target_lang = st.selectbox(
            "Target Language",
            options=[
                ("en", "🇺🇸 English"),
                ("es", "🇪🇸 Spanish"),
                ("fr", "🇫🇷 French"),
                ("de", "🇩🇪 German"),
                ("hi", "🇮🇳 Hindi"),
                ("zh", "🇨🇳 Chinese")
            ],
            format_func=lambda x: x[1]
        )
    
    with col2:
        if st.button("Translate"):
            translated = translate_note_content(text, target_lang[0])
            st.info(f"Translation to {target_lang[1]}:")
            st.write(translated)

# Initialize language on module import
init_language()
