let currentStep = 1;

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
  const price = parseInt(input.dataset.price, 10);
  document.getElementById('summaryPlanPrice').textContent = '$' + price.toLocaleString('es-CL');

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
  document.getElementById('errorModal').classList.add('is-open');
}

function closeErrorModal() {
  document.getElementById('errorModal').classList.remove('is-open');
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
