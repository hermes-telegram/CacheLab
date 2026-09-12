// CacheLab i18n — Language System
window.i18n = {
    current: 'fa',
    
    translations: {
        // ── Navbar ──
        'nav_dashboard': { fa: 'داشبورد', en: 'Dashboard' },
        'nav_core': { fa: 'Core', en: 'Core' },
        'nav_advanced': { fa: 'Advanced', en: 'Advanced' },
        'nav_benchmark': { fa: 'بنچمارک', en: 'Benchmark' },
        'nav_admin': { fa: 'ادمین', en: 'Admin' },
        
        // ── Dashboard ──
        'dash_title': { fa: 'داشبورد زنده', en: 'Live Dashboard' },
        'dash_stats': { fa: 'آمار کلی', en: 'Overview Stats' },
        'dash_total_tests': { fa: 'تعداد تست‌ها', en: 'Total Tests' },
        'dash_hit_rate': { fa: 'نرخ Hit', en: 'Hit Rate' },
        'dash_keys': { fa: 'تعداد کلیدها', en: 'Keys Count' },
        'dash_backends': { fa: 'بک‌اندها', en: 'Backends' },
        'dash_memory': { fa: 'حافظه', en: 'Memory' },
        'dash_disk': { fa: 'دیسک', en: 'Disk' },
        'dash_redis': { fa: 'ردیس', en: 'Redis' },
        'dash_live': { fa: 'مانیتور زنده', en: 'Live Monitor' },
        'dash_recent': { fa: 'آخرین فعالیت‌ها', en: 'Recent Activity' },
        
        // ── Core ──
        'core_title': { fa: 'عملیات پایه کش', en: 'Core Cache Operations' },
        'core_set_get': { fa: 'Set / Get', en: 'Set / Get' },
        'core_ttl': { fa: 'TTL و انقضا', en: 'TTL & Expiry' },
        'core_lru': { fa: 'حذف LRU', en: 'LRU Eviction' },
        'core_bulk': { fa: 'عملیات گروهی', en: 'Bulk Operations' },
        'core_stampede': { fa: 'حفاظت Stampede', en: 'Stampede Protection' },
        'core_multi_tier': { fa: 'Multi-Tier', en: 'Multi-Tier' },
        'core_set_key': { fa: 'کلید', en: 'Key' },
        'core_set_value': { fa: 'مقدار', en: 'Value' },
        'core_set_ttl': { fa: 'TTL (ثانیه)', en: 'TTL (seconds)' },
        'core_set_btn': { fa: 'ذخیره', en: 'Save' },
        'core_get_btn': { fa: 'بازیابی', en: 'Get' },
        'core_delete_btn': { fa: 'حذف', en: 'Delete' },
        'core_clear_btn': { fa: 'پاک کردن همه', en: 'Clear All' },
        'core_result': { fa: 'نتیجه', en: 'Result' },
        
        // ── Advanced ──
        'adv_title': { fa: 'الگوهای پیشرفته', en: 'Advanced Patterns' },
        'adv_subtitle': { fa: 'هر الگو تعاملی است و با کتابخانه recall واقعی اجرا می‌شود', en: 'Each pattern is interactive and runs against the real recall library' },
        'adv_test': { fa: 'تست', en: 'Test' },
        
        // ── Benchmark ──
        'bench_title': { fa: 'بنچمارک عملکرد', en: 'Performance Benchmark' },
        'bench_run': { fa: 'اجرای بنچمارک', en: 'Run Benchmark' },
        'bench_results': { fa: 'نتایج', en: 'Results' },
        
        // ── Admin ──
        'admin_title': { fa: 'پنل مدیریت', en: 'Admin Panel' },
        
        // ── Common ──
        'loading': { fa: 'در حال بارگذاری...', en: 'Loading...' },
        'running': { fa: 'در حال اجرا...', en: 'Running...' },
        'success': { fa: 'موفق', en: 'Success' },
        'error': { fa: 'خطا', en: 'Error' },
        'copy': { fa: 'کپی', en: 'Copy' },
    },
    
    t(key) {
        const item = this.translations[key];
        if (!item) return key;
        return item[this.current] || item['fa'] || key;
    },
    
    setLang(lang) {
        this.current = lang;
        localStorage.setItem('cachelab_lang', lang);
        this.apply();
    },
    
    init() {
        const saved = localStorage.getItem('cachelab_lang');
        if (saved) this.current = saved;
        this.apply();
    },
    
    apply() {
        const isEN = this.current === 'en';
        document.documentElement.lang = isEN ? 'en' : 'fa';
        document.documentElement.dir = isEN ? 'ltr' : 'rtl';
        document.body.dir = isEN ? 'ltr' : 'rtl';
        document.body.style.fontFamily = isEN ? "'Inter', 'Segoe UI', sans-serif" : "'Vazirmatn', sans-serif";
        
        // Update all elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            const text = this.t(key);
            if (text) el.textContent = text;
        });
        
        // Update all elements with data-i18n-html
        document.querySelectorAll('[data-i18n-html]').forEach(el => {
            const key = el.getAttribute('data-i18n-html');
            const html = this.t(key);
            if (html) el.innerHTML = html;
        });
        
        // Update lang toggle button
        const btn = document.getElementById('langToggle');
        if (btn) btn.innerHTML = isEN ? '<i class="fas fa-globe"></i> FA' : '<i class="fas fa-globe"></i> EN';
    }
};

// Auto-init
document.addEventListener('DOMContentLoaded', () => window.i18n.init());
