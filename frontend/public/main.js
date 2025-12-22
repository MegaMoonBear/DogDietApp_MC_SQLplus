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

  // Populate searchable breed datalist from API so the list stays in sync with the database
  // Critical: `fetch('/api/breeds')` must return JSON with a `breeds` array of objects containing `breed_name_AKC`.
  const breedInput = document.getElementById('breed_name');
  const breedDatalist = document.getElementById('breed_list');
  if (breedInput && breedDatalist) {
    fetch('/api/breeds')
      .then((response) => (response.ok ? response.json() : Promise.reject()))
      .then((data) => {
        const breeds = data?.breeds || [];
        breeds.forEach((b) => {
          // Initial use: add option.value as breed name so datalist suggestions map directly to input value
          const option = document.createElement('option');
          option.value = b.breed_name_AKC;
          breedDatalist.appendChild(option);
        });
      })
      .catch(() => {
        // No-op fallback: leave input as free-text if API fails; users can still submit manually
      });
  }

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
        const response = await fetch('/api/submit', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        });

        if (response.ok) {
          const result = await response.json();
          const aiResults = document.getElementById('aiQuestionsResult');
          if (aiResults) {
            aiResults.innerHTML = '';
            result.questions.forEach((q) => {
              const p = document.createElement('p');
              p.textContent = q;
              aiResults.appendChild(p);
            });
          }
        } else {
          alert('Failed to submit the form. Please try again.');
        }
      } catch (error) {
        console.error('Submission error:', error);
        const aiResults = document.getElementById('aiQuestionsResult');
        if (aiResults) aiResults.innerHTML = '<h3 class="ai-results-title">AI-Generated Vet Questions</h3><p class="ai-results-disclaimer">Three simple, educational questions to discuss with your veterinarian. This is informational only — not medical advice.</p><div class="ai-results-body">Failed to submit form. Please check your connection.</div>';
      }
    });
  }

/*
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
*/
});
