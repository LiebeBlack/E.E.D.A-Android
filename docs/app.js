// E.E.D.A. JavaScript Engine - Simplified and Working
console.log('🚀 E.E.D.A. Loading...');

// Global State
const APP_STATE = {
    theme: localStorage.getItem('eeda-theme') || 'dark',
    isInitialized: false
};

// Utility Functions
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// Theme Controller
class ThemeController {
    constructor() {
        this.themeToggle = $('#themeToggle');
        this.init();
    }

    init() {
        this.setTheme(APP_STATE.theme);
        this.themeToggle?.addEventListener('click', () => this.toggleTheme());
    }

    setTheme(theme) {
        APP_STATE.theme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('eeda-theme', theme);
    }

    toggleTheme() {
        const newTheme = APP_STATE.theme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }
}

// Magnetic Hover Effect
class MagneticHover {
    constructor() {
        this.elements = $$('.magnetic-btn');
        this.init();
    }

    init() {
        this.elements.forEach(element => {
            element.addEventListener('mouseenter', this.handleMouseEnter.bind(this));
            element.addEventListener('mousemove', this.handleMouseMove.bind(this));
            element.addEventListener('mouseleave', this.handleMouseLeave.bind(this));
        });
    }

    handleMouseEnter(e) {
        const element = e.currentTarget;
        element.style.transition = 'none';
    }

    handleMouseMove(e) {
        const element = e.currentTarget;
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        const deltaX = (e.clientX - centerX) * 0.15;
        const deltaY = (e.clientY - centerY) * 0.15;
        
        element.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
        
        const glow = element.querySelector('.btn-glow');
        if (glow) {
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            glow.style.setProperty('--mouse-x', `${x}%`);
            glow.style.setProperty('--mouse-y', `${y}%`);
        }
    }

    handleMouseLeave(e) {
        const element = e.currentTarget;
        element.style.transition = 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        element.style.transform = 'translate(0, 0)';
    }
}

// Scroll Reveal
class ScrollReveal {
    constructor() {
        this.elements = $$('.scroll-reveal');
        this.init();
    }

    init() {
        this.createObserver();
        this.observeElements();
    }

    createObserver() {
        const options = {
            root: null,
            rootMargin: '-5% 0px -5% 0px',
            threshold: 0.1
        };

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.revealElement(entry.target);
                }
            });
        }, options);
    }

    observeElements() {
        this.elements.forEach(element => {
            this.observer.observe(element);
        });
    }

    revealElement(element) {
        element.classList.add('revealed');
        this.observer.unobserve(element);
    }
}

// Terminal Controller
class TerminalController {
    constructor() {
        this.tabButtons = $$('.tab-btn');
        this.tabContents = $$('.tab-content');
        this.copyButtons = $$('.copy-btn');
        this.init();
    }

    init() {
        // Tab switching
        this.tabButtons.forEach(button => {
            button.addEventListener('click', (e) => this.switchTab(e));
        });

        // Copy to clipboard
        this.copyButtons.forEach(button => {
            button.addEventListener('click', (e) => this.copyToClipboard(e));
        });
    }

    switchTab(e) {
        const targetTab = e.target.dataset.tab;
        
        // Update button states
        this.tabButtons.forEach(btn => btn.classList.remove('active'));
        e.target.classList.add('active');
        
        // Update content visibility
        this.tabContents.forEach(content => {
            content.classList.remove('active');
            if (content.id === `tab-${targetTab}`) {
                content.classList.add('active');
            }
        });
    }

    async copyToClipboard(e) {
        const button = e.currentTarget;
        const text = button.dataset.clipboard;
        
        if (!text) return;

        try {
            await navigator.clipboard.writeText(text);
            this.showCopyFeedback(button);
        } catch (err) {
            // Fallback
            this.fallbackCopy(text);
            this.showCopyFeedback(button);
        }
    }

    fallbackCopy(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
    }

    showCopyFeedback(button) {
        button.classList.add('copied');
        setTimeout(() => {
            button.classList.remove('copied');
        }, 2000);
    }
}

// Navigation Controller
class NavigationController {
    constructor() {
        this.navLinks = $$('a[href^="#"]');
        this.header = $('.main-nav');
        this.init();
    }

    init() {
        // Smooth scrolling
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => this.handleSmoothScroll(e));
        });
    }

    handleSmoothScroll(e) {
        const href = e.currentTarget.getAttribute('href');
        const target = $(href);
        
        if (target) {
            e.preventDefault();
            const headerHeight = this.header?.offsetHeight || 0;
            const targetPosition = target.offsetTop - headerHeight - 20;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    }
}

// Bento Card Glow Effect
class BentoCardGlow {
    constructor() {
        this.cards = $$('.bento-card');
        this.init();
    }

    init() {
        this.cards.forEach(card => {
            card.addEventListener('mousemove', this.handleMouseMove.bind(this));
            card.addEventListener('mouseleave', this.handleMouseLeave.bind(this));
        });
    }

    handleMouseMove(e) {
        const card = e.currentTarget;
        const rect = card.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        
        const glow = card.querySelector('.card-glow');
        if (glow) {
            glow.style.setProperty('--mouse-x', `${x}%`);
            glow.style.setProperty('--mouse-y', `${y}%`);
        }
    }

    handleMouseLeave(e) {
        const card = e.currentTarget;
        const glow = card.querySelector('.card-glow');
        if (glow) {
            glow.style.setProperty('--mouse-x', '50%');
            glow.style.setProperty('--mouse-y', '50%');
        }
    }
}

// Mobile Menu Controller
class MobileMenuController {
    constructor() {
        this.menuToggle = $('#mobileMenuToggle');
        this.navLinks = $('#navLinks');
        this.init();
    }

    init() {
        if (this.menuToggle) {
            this.menuToggle.addEventListener('click', () => this.toggleMenu());
        }

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (this.navLinks && this.navLinks.classList.contains('active')) {
                if (!this.navLinks.contains(e.target) && !this.menuToggle.contains(e.target)) {
                    this.closeMenu();
                }
            }
        });

        // Close menu when clicking on a link
        const links = this.navLinks?.querySelectorAll('.nav-link');
        links?.forEach(link => {
            link.addEventListener('click', () => this.closeMenu());
        });
    }

    toggleMenu() {
        this.navLinks?.classList.toggle('active');
        this.menuToggle?.classList.toggle('active');
    }

    closeMenu() {
        this.navLinks?.classList.remove('active');
        this.menuToggle?.classList.remove('active');
    }
}

// Main App Controller
class EEDAApp {
    constructor() {
        this.controllers = [];
        this.init();
    }

    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.start());
        } else {
            this.start();
        }
    }

    start() {
        try {
            console.log('🚀 Initializing E.E.D.A. Frontend Engine...');
            
            // Initialize controllers
            this.controllers.push(new ThemeController());
            this.controllers.push(new MobileMenuController());
            this.controllers.push(new MagneticHover());
            this.controllers.push(new ScrollReveal());
            this.controllers.push(new TerminalController());
            this.controllers.push(new NavigationController());
            this.controllers.push(new BentoCardGlow());

            // Initialize Lucide icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }

            // Mark as initialized
            APP_STATE.isInitialized = true;
            console.log('✅ E.E.D.A. Frontend Engine initialized successfully');

        } catch (error) {
            console.error('❌ Failed to initialize E.E.D.A.:', error);
        }
    }
}

// Initialize app when DOM is ready
window.EEDA = new EEDAApp();

// Show content immediately
document.addEventListener('DOMContentLoaded', () => {
    document.body.style.opacity = '1';
});
