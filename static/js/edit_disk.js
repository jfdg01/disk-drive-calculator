// edit_disk.js
document.addEventListener('DOMContentLoaded', () => {
    const mainStatsMap = {
        1: ["Flat HP"],
        2: ["Flat ATK"],
        3: ["Flat DEF"],
        4: ["HP%", "ATK%", "DEF%", "CRIT Rate", "CRIT DMG", "Anomaly Proficiency"],
        5: ["HP%", "ATK%", "DEF%", "PEN Ratio", "Element DMG Bonus"],
        6: ["HP%", "ATK%", "DEF%", "Anomaly Mastery", "Impact", "Energy Regen%"]
    };

    const slotSelect = document.getElementById('slot');
    const mainStatSelect = document.getElementById('main_stat');

    // Update Main Stat options when Slot changes
    slotSelect.addEventListener('change', () => {
        const selectedSlot = parseInt(slotSelect.value);
        const options = mainStatsMap[selectedSlot] || [];

        // Clear and update Main Stat dropdown
        mainStatSelect.innerHTML = '';
        options.forEach(stat => {
            const option = document.createElement('option');
            option.value = stat;
            option.textContent = stat;
            mainStatSelect.appendChild(option);
        });
    });

    // Trigger change event to initialize correct options on page load
    slotSelect.dispatchEvent(new Event('change'));
});