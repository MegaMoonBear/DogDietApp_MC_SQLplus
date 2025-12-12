document.addEventListener('DOMContentLoaded', () => {
  const dogForm = document.getElementById('dogQuestionnaireForm');
  const adminForm = document.getElementById('adminUpdateForm');

  const parseJson = async (response) => {
    try {
      return await response.json();
    } catch {
      return {};
    }
  };

  if (dogForm) {
    dogForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const formData = new FormData(dogForm);
      const payload = {
        breed_name_AKC: formData.get('breed_name_AKC')?.trim(),
        age_years_preReg: parseFloat(formData.get('age_years_preReg')),
        status_dietRelat_preReg: formData.getAll('status_dietRelat_preReg'),
      };

      if (!payload.breed_name_AKC || Number.isNaN(payload.age_years_preReg)) {
        alert('Please enter a breed name and age.');
        return;
      }

      try {
        const response = await fetch('/api/submit-dog-info', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });

        const result = await parseJson(response);

        if (response.ok) {
          alert(result.message ? `Success! ${result.message}` : 'Submitted successfully.');
          dogForm.reset();
        } else {
          alert(result.detail ? `Error: ${result.detail}` : 'Error submitting form.');
        }
      } catch (error) {
        console.error('Submission error:', error);
        alert('Failed to submit form. Please check your connection.');
      }
    });
  }

  if (adminForm) {
    adminForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const formData = new FormData(adminForm);
      const searchField = formData.get('search_field');
      const searchValue = formData.get('search_value')?.trim();
      const updateData = {};

      for (const [key, value] of formData.entries()) {
        if (key === 'search_field' || key === 'search_value') continue;
        if (value === null || value === '') continue;
        updateData[key] = value;
      }

      if (!searchValue) {
        alert('Please provide a search value.');
        return;
      }

      if (Object.keys(updateData).length === 0) {
        alert('Please fill in at least one field to update.');
        return;
      }

      try {
        const response = await fetch(`/api/breed/${searchField}/${encodeURIComponent(searchValue)}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(updateData),
        });

        const result = await parseJson(response);

        if (response.ok) {
          alert('Success! Breed information updated.');
          adminForm.reset();
        } else {
          alert(result.error ? `Error: ${result.error}` : 'Update failed.');
        }
      } catch (error) {
        console.error('Admin update error:', error);
        alert('Failed to update breed information. Please try again.');
      }
    });
  }
});
