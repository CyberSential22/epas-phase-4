/**
 * Password Strength Meter - Phase 4.5
 * Provides real-time feedback on password complexity.
 */
document.addEventListener('DOMContentLoaded', () => {
    const passwordInput = document.getElementById('password');
    const strengthBar = document.getElementById('strength-bar');
    const strengthText = document.getElementById('strength-text');

    if (!passwordInput || !strengthBar || !strengthText) return;

    passwordInput.addEventListener('input', () => {
        const val = passwordInput.value;
        const result = checkStrength(val);
        
        // Update Bar
        strengthBar.style.width = result.percent + '%';
        strengthBar.style.backgroundColor = result.color;
        
        // Update Text
        strengthText.innerText = `Strength: ${result.label}`;
        strengthText.style.color = result.color;
    });

    function checkStrength(password) {
        let score = 0;
        if (!password) return { percent: 0, label: 'Empty', color: '#cbd5e1' };

        // length
        if (password.length >= 8) score += 1;
        if (password.length >= 12) score += 1;

        // character classes
        if (/[a-z]/.test(password)) score += 1;
        if (/[A-Z]/.test(password)) score += 1;
        if (/[0-9]/.test(password)) score += 1;
        if (/[^A-Za-z0-9]/.test(password)) score += 1;

        // Map score (0-6) to UI
        if (score < 3) return { percent: 25, label: 'Weak', color: '#ef4444' }; // Red
        if (score < 4) return { percent: 50, label: 'Fair', color: '#f59e0b' }; // Orange
        if (score < 5) return { percent: 75, label: 'Good', color: '#3b82f6' }; // Blue/Yellow-ish
        return { percent: 100, label: 'Strong', color: '#10b981' }; // Green
    }
});
