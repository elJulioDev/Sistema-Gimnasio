let currentStep = 1;

const birthDateInput = document.getElementById('birthDate');
const ageDisplay = document.getElementById('ageDisplay');

const MIN_AGE = 15;
const MAX_AGE = 100;

const today = new Date();
const formattedToday = today.toISOString().split('T')[0];
if (birthDateInput) {
    birthDateInput.max = formattedToday;
}

if (birthDateInput && ageDisplay) {
    birthDateInput.addEventListener('change', function() {
        const edadHidden = document.getElementById('edadHidden');
        if (!this.value) {
            ageDisplay.innerHTML = '';
            this.setCustomValidity('');
            if (edadHidden) edadHidden.value = '';
            return;
        }

        const dob = new Date(this.value);
        let age = today.getFullYear() - dob.getFullYear();
        const m = today.getMonth() - dob.getMonth();

        if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
            age--;
        }

        if (age < MIN_AGE) {
            ageDisplay.innerHTML = `<i class="bi bi-x-circle"></i> Lo sentimos, debes tener al menos ${MIN_AGE} años. (Tienes ${age})`;
            ageDisplay.className = 'd-block mt-1 text-danger';
            this.setCustomValidity(`Debes ser mayor de ${MIN_AGE} años.`);
        } else if (age > MAX_AGE || age < 0) {
            ageDisplay.innerHTML = `<i class="bi bi-exclamation-triangle"></i> Por favor ingresa una fecha válida.`;
            ageDisplay.className = 'd-block mt-1 text-danger';
            this.setCustomValidity('Fecha inválida.');
        } else {
            ageDisplay.innerHTML = `<i class="bi bi-check2-circle"></i> Tienes ${age} años.`;
            ageDisplay.className = 'd-block mt-1 text-accent-volt';
            this.setCustomValidity('');
            if (edadHidden) edadHidden.value = age;
        }
    });
}

function fechaLocalISO(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

(function () {
  const dob = document.getElementById('fechaNacimiento');
  if (!dob) return;
  const hoy = new Date();
  dob.max = fechaLocalISO(hoy);
  dob.min = fechaLocalISO(new Date(hoy.getFullYear() - 90, hoy.getMonth(), hoy.getDate()));
})();

function goToStep(step) {
  document.querySelectorAll('.step-panel').forEach(p => p.classList.remove('active'));
  document.getElementById('step' + step).classList.add('active');

  document.querySelectorAll('.step-item').forEach(item => {
    const n = parseInt(item.dataset.step, 10);
    item.classList.toggle('active', n === step);
    item.classList.toggle('completed', n < step);
  });

  currentStep = step;
}

function nextStep() {
  if (currentStep === 2 && !validateStep2()) return;
  goToStep(currentStep + 1);
}

function prevStep() {
  goToStep(currentStep - 1);
}

function selectPlan(input) {
    document.getElementById('btnStep1').disabled = false;
    document.getElementById('summaryPlanName').textContent = input.dataset.name;
    document.getElementById('summaryPlanPrice').textContent = '$' + formatCurrencyCLP(input.dataset.price);
    const esEstudiante = input.value === 'estudiante';
    document.getElementById('certificadoGroup').style.display = esEstudiante ? 'flex' : 'none';
    if (!esEstudiante) removeCertificado();
}

function validateStep2() {
  const form = document.getElementById('registerForm');
  const requiredFields = document.querySelectorAll('#step2 [required]');
  const fechaNacimiento = form.querySelector('[name="fecha_nacimiento"]').value;
  if (fechaNacimiento > fechaLocalISO(new Date())) {
    showErrorModal('Fecha inválida', 'La fecha de nacimiento no puede ser futura.');
    return false;
  }
  for (const field of requiredFields) {
    if (!field.value.trim()) {
      showErrorModal('Faltan datos', 'Completa todos los campos obligatorios antes de continuar.');
      field.focus();
      return false;
    }
  }

  const password = form.querySelector('[name="password"]').value;
  const confirm = form.querySelector('[name="confirmar_password"]').value;
  if (password !== confirm) {
    showErrorModal('Contraseñas no coinciden', 'Revisa que ambas contraseñas sean idénticas.');
    return false;
  }

  if (!document.getElementById('consentCheck').checked) {
    showErrorModal('Consentimiento requerido', 'Debes aceptar el tratamiento de tus datos personales para continuar, según la Ley N° 19.628 y su reforma, la Ley N° 21.719.');
    return false;
  }

  return true;
}

function enablePayment() {
  document.getElementById('btnPayment').disabled = false;
}

function processPayment() {
  // Placeholder visual: aquí se conectará la pasarela real
  goToStep(4);
}

function openPrivacyModal(e) {
  e.preventDefault();
  document.getElementById('privacyModal').classList.add('is-open');
}

function closePrivacyModal() {
  document.getElementById('privacyModal').classList.remove('is-open');
}

function showErrorModal(title, message) {
  document.getElementById('errorModalTitle').textContent = title;
  document.getElementById('errorModalMessage').textContent = message;
  bootstrap.Modal.getOrCreateInstance(document.getElementById('errorModal')).show();
}

function closeErrorModal() {
  const modal = bootstrap.Modal.getInstance(document.getElementById('errorModal'));
  if (modal) modal.hide();
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closePrivacyModal();
    closeErrorModal();
  }
});

function actualizarEdad() {
  const input = document.getElementById('fechaNacimiento');
  const preview = document.getElementById('edadPreview');
  if (!input.value) { preview.textContent = ''; return; }

  const [anio, mes, dia] = input.value.split('-').map(Number);
  const hoy = new Date();
  let edad = hoy.getFullYear() - anio;
  const sinCumplir = (hoy.getMonth() + 1) < mes || ((hoy.getMonth() + 1) === mes && hoy.getDate() < dia);
  if (sinCumplir) edad--;

  preview.textContent = edad >= 0 ? `Tienes ${edad} años` : '';
}

function formatCurrencyCLP(value) {
    let strValue = String(value).trim();
    strValue = strValue.replace(/[.,]\d{1,2}$/, '');
    const cleanValue = strValue.replace(/[.,]/g, '');
    const finalNumber = parseInt(cleanValue, 10);
    return isNaN(finalNumber) ? '0' : finalNumber.toLocaleString('es-CL');
}

function handleCertificadoChange(input) {
  const file = input.files[0];
  if (!file) return;

  if (file.type !== 'application/pdf') {
    showErrorModal('Archivo inválido', 'El certificado debe ser un PDF.');
    input.value = '';
    return;
  }
  if (file.size > 5 * 1024 * 1024) {
    showErrorModal('Archivo muy pesado', 'El certificado no puede superar 5MB.');
    input.value = '';
    return;
  }

  const zone = document.getElementById('fileUploadZone');
  zone.classList.add('has-file');
  zone.querySelector('i').className = 'bi bi-file-earmark-check-fill';
  document.getElementById('fileUploadText').textContent = file.name;
  document.getElementById('fileUploadRemove').hidden = false;
}

function removeCertificado(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  document.getElementById('certificadoInput').value = '';
  const zone = document.getElementById('fileUploadZone');
  zone.classList.remove('has-file');
  zone.querySelector('i').className = 'bi bi-cloud-arrow-up';
  document.getElementById('fileUploadText').textContent = 'Arrastra tu PDF aquí o haz clic para subirlo';
  document.getElementById('fileUploadRemove').hidden = true;
}

const fileZone = document.getElementById('fileUploadZone');
if (fileZone) {
  fileZone.addEventListener('dragover', (e) => { e.preventDefault(); fileZone.classList.add('is-dragover'); });
  fileZone.addEventListener('dragleave', () => fileZone.classList.remove('is-dragover'));
  fileZone.addEventListener('drop', (e) => {
    e.preventDefault();
    fileZone.classList.remove('is-dragover');
    if (!e.dataTransfer.files[0]) return;
    document.getElementById('certificadoInput').files = e.dataTransfer.files;
    handleCertificadoChange(document.getElementById('certificadoInput'));
  });
}

document.addEventListener('DOMContentLoaded', () => {
    const steps = document.querySelectorAll('.step-content');
    const indicators = document.querySelectorAll('.register-progress .step');
    const progressTrack = document.querySelector('.progress-track');
    const nextBtns = document.querySelectorAll('.btn-next');
    const prevBtns = document.querySelectorAll('.btn-prev');
    const finishBtn = document.querySelector('.btn-finish');

    let currentStep = Array.from(steps).findIndex(s => s.classList.contains('active'));
    if (currentStep === -1) currentStep = 0;

    const jumpInput = document.getElementById('jumpToStep');
    if (jumpInput && jumpInput.value) {
        currentStep = parseInt(jumpInput.value, 10) - 1;
    }

    function updateProgress() {
        // Actualiza la línea de progreso
        const percentage = (currentStep / (steps.length - 1)) * 100;
        progressTrack.style.width = `${percentage}%`;

        // Actualiza los círculos y contenidos
        steps.forEach((step, i) => {
            step.classList.toggle('d-none', i !== currentStep);
            step.classList.toggle('active', i === currentStep);
        });

        indicators.forEach((ind, i) => {
            ind.classList.toggle('active', i <= currentStep);
            // Si el paso ya pasó, cambiar estilo
            if(i < currentStep) {
                ind.classList.add('completed');
            } else {
                ind.classList.remove('completed');
            }
        });
    }

    nextBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const currentFormStep = steps[currentStep];
            const inputs = currentFormStep.querySelectorAll('input[required]');
            let valid = true;

            inputs.forEach(input => {
                if (!input.checkValidity()) {
                    input.reportValidity();
                    valid = false;
                }
            });

            // Lógica Exclusiva al intentar salir del Paso 2 (índice 1)
            if (valid && currentStep === 1) {
                const form = document.getElementById('registerForm');
                
                // 1. Validar que las contraseñas coincidan localmente
                const password = form.querySelector('[name="password"]').value;
                const confirm = form.querySelector('[name="confirmar_password"]').value;
                if (password !== confirm) {
                    showErrorModal('Error en contraseñas', 'Revisa que ambas contraseñas sean idénticas.');
                    return; // Detiene el avance al paso 3
                }

                // 2. Validar que aceptó el consentimiento
                const consentData = document.getElementById('consentData');
                if (consentData && !consentData.checked) {
                    showErrorModal('Consentimiento requerido', 'Debes aceptar el tratamiento de tus datos para continuar.');
                    return; // Detiene el avance al paso 3
                }

                // 3. Consulta asíncrona a Django para validar RUT y Correo
                const rut = form.querySelector('[name="rut"]').value;
                const email = form.querySelector('[name="email"]').value;
                
                try {
                    // Cambiamos estado del botón temporalmente
                    const originalText = btn.innerHTML;
                    btn.innerHTML = 'Validando...';
                    btn.disabled = true;

                    const response = await fetch(`/validar-usuario/?rut=${encodeURIComponent(rut)}&email=${encodeURIComponent(email)}`);
                    const data = await response.json();

                    // Restauramos estado del botón
                    btn.innerHTML = originalText;
                    btn.disabled = false;

                    if (!data.valido) {
                        // Aquí se lanza el modal con el error ("Ya existe una cuenta con ese RUT")
                        showErrorModal('Datos ya registrados', data.mensaje);
                        return; // Evita avanzar al paso 3
                    }
                } catch (error) {
                    console.error('Error de validación contra el servidor:', error);
                    btn.disabled = false;
                }
            }

            // Si todo está correcto (valid = true y servidor devolvió data.valido = true) avanza
            if (valid && currentStep < steps.length - 1) {
                currentStep++;
                updateProgress();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    });

    prevBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (currentStep > 0) {
                currentStep--;
                updateProgress();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    });

    function syncOrderSummary() {
        const checked = document.querySelector('input[name="plan"]:checked');
        if (!checked) return;
        const card = checked.closest('.plan-option').querySelector('.plan-detail-card');
        const nameEl = document.getElementById('summaryPlanName');
        const priceEl = document.getElementById('summaryPlanPrice');
        if (nameEl) nameEl.textContent = card.dataset.name;
        if (priceEl) priceEl.textContent = '$' + formatCurrencyCLP(card.dataset.price) + '/mes';
    }

    updateProgress();

    // Selección de plan: todo el card es clickable, no requiere botón aparte
    const planCards = document.querySelectorAll('.plan-detail-card');

    function selectPlanCard(card) {
        const radio = card.closest('.plan-option').querySelector('input[type="radio"]');
        radio.checked = true;
        planCards.forEach(c => c.classList.remove('is-selected'));
        card.classList.add('is-selected');
        syncOrderSummary();
    }

    planCards.forEach(card => {
        card.addEventListener('click', (e) => {
            if (e.target.closest('.plan-detail-card__toggle')) return;
            selectPlanCard(card);
            card.classList.remove('is-open');
        });
    });

    document.querySelectorAll('.plan-detail-card__toggle').forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            const card = toggle.closest('.plan-detail-card');
            const wasOpen = card.classList.contains('is-open');
            planCards.forEach(c => c.classList.remove('is-open'));
            if (!wasOpen) card.classList.add('is-open');
        });
    });

    document.querySelectorAll('.raw-price').forEach(el => {
        el.textContent = formatCurrencyCLP(el.textContent);
    });

    // Carrusel de planes: transform-based, con flechas, dots y arrastre (mouse/touch)
    const track = document.getElementById('planTrack');
    const slides = document.querySelectorAll('.plan-carousel__slide');
    const dots = document.querySelectorAll('.plan-carousel__dot');
    const prevBtn = document.querySelector('.plan-carousel__nav--prev');
    const nextBtn = document.querySelector('.plan-carousel__nav--next');
    let dragStartX = 0;
    let dragDeltaX = 0;
    let isDragging = false;

    let activeSlide = 1;
    const checkedRadio = document.querySelector('input[name="plan"]:checked');
    if (checkedRadio) {
        const slide = checkedRadio.closest('.plan-carousel__slide');
        if (slide) {
            activeSlide = parseInt(slide.dataset.slide, 10);
        }
    }

    function goToSlide(index) {
        activeSlide = Math.max(0, Math.min(slides.length - 1, index));
        track.style.transform = `translateX(-${activeSlide * 100}%)`;
        dots.forEach((d, i) => d.classList.toggle('is-active', i === activeSlide));
    }

    if (track && prevBtn && nextBtn) {
        prevBtn.addEventListener('click', () => goToSlide(activeSlide - 1));
        nextBtn.addEventListener('click', () => goToSlide(activeSlide + 1));
        dots.forEach(dot => {
            dot.addEventListener('click', () => goToSlide(parseInt(dot.dataset.dot, 10)));
        });

        function dragStart(clientX) {
            if (!window.matchMedia('(min-width: 768px)').matches) return;
            isDragging = true;
            dragStartX = clientX;
            dragDeltaX = 0;
            track.classList.add('is-dragging');
        }
        function dragMove(clientX) {
            if (!isDragging) return;
            dragDeltaX = clientX - dragStartX;
            const percent = (dragDeltaX / track.offsetWidth) * 100;
            track.style.transform = `translateX(calc(-${activeSlide * 100}% + ${percent}%))`;
        }
        function dragEnd() {
            if (!isDragging) return;
            isDragging = false;
            track.classList.remove('is-dragging');
            const threshold = track.offsetWidth * 0.15;
            if (dragDeltaX > threshold) {
                goToSlide(activeSlide - 1);
            } else if (dragDeltaX < -threshold) {
                goToSlide(activeSlide + 1);
            } else {
                goToSlide(activeSlide);
            }
        }

        track.addEventListener('mousedown', (e) => { e.preventDefault(); dragStart(e.clientX); });
        window.addEventListener('mousemove', (e) => dragMove(e.clientX));
        window.addEventListener('mouseup', dragEnd);

        track.addEventListener('touchstart', (e) => dragStart(e.touches[0].clientX), { passive: true });
        track.addEventListener('touchmove', (e) => dragMove(e.touches[0].clientX), { passive: true });
        track.addEventListener('touchend', dragEnd);

        goToSlide(activeSlide);
    }

    // Estilización métodos de pago
    const bankCards = document.querySelectorAll('.bank-card');
    bankCards.forEach(card => {
        card.addEventListener('click', () => {
            bankCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            document.getElementById('metodoPagoInput').value = card.dataset.method;
        });
    });

    syncOrderSummary();
});