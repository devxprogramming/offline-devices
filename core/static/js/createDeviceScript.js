const bankSelector = document.getElementById('selectBank');
const branchContainer = document.getElementById('branchContainer');

const saveDeviceBtn = document.getElementById("saveDevice");


const BANK_API = 'http://localhost:8000/api/v1/banks/';
const BRANCH_API = 'http://localhost:8000/api/v1/branches/';

async function fetchBanks() {
    try {
        const response = await fetch(BANK_API);
        const data = await response.json();
        if (data.length > 0) {
            data.forEach(bank => {
                const option = document.createElement('option');
                option.value = bank.id;
                option.text = bank.name;
                bankSelector.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error fetching banks:', error);
    }
}

async function fetchBranches(bankId) {
    try {
        const response = await fetch(`${BRANCH_API}?bank_id=${bankId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching branches:', error);
        return [];
    }
}

function ensureBranchSelector() {
    let branchSelect = document.getElementById('selectBranch');
    let branchSelectLabel = document.getElementById('branch-select-label');
    if (!branchSelectLabel) {
        branchSelectLabel = document.createElement('label');
        branchSelectLabel.id = 'branch-select-label';
        branchSelectLabel.textContent = 'Select Branch';
        branchContainer.appendChild(branchSelectLabel);
    }
    if (!branchSelect) {
        branchSelect = document.createElement('select');
        branchSelect.id = 'selectBranch';
        branchSelect.name = 'branch_select';
        branchSelect.classList.add('form-select');

        // Optionally add a label if needed (but you already have it in your HTML form)
        branchContainer.appendChild(branchSelect);
    }
    return branchSelect;
}

function updateBranchSelector(branches) {
    const branchSelect = ensureBranchSelector();

    // Clear existing options
    branchSelect.innerHTML = '';

    // Add default option
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Select a Branch';
    branchSelect.appendChild(defaultOption);

    // Add branches
    branches.forEach(branch => {
        const option = document.createElement('option');
        option.value = branch.id;
        option.textContent = branch.branch_name;
        branchSelect.appendChild(option);
    });
}

bankSelector.addEventListener('change', async function () {
    const bankId = this.value;
    if (bankId) {
        const branches = await fetchBranches(bankId);
        updateBranchSelector(branches);
    } else {
        const branchSelect = document.getElementById('selectBranch');
        if (branchSelect) {
            branchSelect.innerHTML = '';  // Clear options if no bank selected
        }
    }
});



// Save device
saveDeviceBtn.addEventListener('click', async function () {
    try{
        const response = await fetch('http://localhost:8000/api/v1/devices/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                serial_number: document.getElementById('serial_number').value,
                // bank: document.getElementById('selectBank').value,
                branch: document.getElementById('selectBranch').value,
            }),
        })
    }
    catch(error){
        // alert the user of the error
        alert( "Error saving device: " + error);
    }
    finally{
        // reload the page
        location.reload();
    }
});



document.addEventListener('DOMContentLoaded', () => {
    fetchBanks();
});
