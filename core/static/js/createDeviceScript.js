const bankSelector = document.getElementById('selectBank');
const branchContainer = document.getElementById('branchContainer');

const saveDeviceBtn = document.getElementById("saveDevice");


const BRANCH_API = 'http://localhost:8000/api/v1/branches/';
const BANK_API = 'http://localhost:8000/api/v1/banks/'

async function fetchBranches(bank_id){
    const url = bank_id ?  `${BRANCH_API}?bank_id=${bank_id}` : BRANCH_API

    const res = await fetch(
        url,
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        }
    )

    if (!res.ok){
        throw new Error(`Error Fetching branches: ${res.status} ${res.statusText}`)
    }
    return res.json()
    
}



// Manupulate the DOM.

// fetch banks in to the select element.

const fetchBanks = async () => {
    try{
        
        const res = await fetch(
            BANK_API,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        )
        if (!res.ok){
            throw new Error(`Error: ${error.status} ${error.statusText}`)
        }

        const jsonRes = await res.json()
        
        return jsonRes
    }
    catch(error){
        throw new Error(`Encountred Errors: ${error.status} ${error.statusText}`)
    }
}




document.addEventListener('DOMContentLoaded', async () => {
  try {
    const banks = await fetchBanks(); 
    banks.forEach(bank => {
      const opt = document.createElement('option');
      opt.value = bank.id;
      opt.textContent = bank.name;
      bankSelector.appendChild(opt);
    });
  } catch (error) {
    console.error(error);
    alert(`Failed to load banks: ${error.message}`);
  }
});


// When user selects a bank, fetch and render its branches
bankSelector.addEventListener('change', async (event) => {
  try {
    const bankId   = event.target.value;
    const data     = await fetchBranches(bankId);
    const branches = data.branches || [];

    branchContainer.innerHTML = '';

    // If no branches, we simply do nothing (no select shown)
    if (branches.length === 0) {
      return;
    }

    const selectLabel = document.createElement('label')
    selectLabel.textContent = "Select Branch"
    selectLabel.setAttribute('for', "selectBranch")

    const selectBranch = document.createElement('select');
    selectBranch.classList.add('form-select')
    selectBranch.id = 'selectBranch';

    // placeholder
    const placeholder = document.createElement('option');
    placeholder.value       = '';
    placeholder.textContent = 'Select a branch…';
    placeholder.disabled    = true;
    placeholder.selected    = true;
    selectBranch.appendChild(placeholder);
    
    // real options
    branches.forEach(branch => {
        const opt = document.createElement('option');
        opt.value       = branch.id;
        opt.textContent = branch.branch_name;
        selectBranch.appendChild(opt);
    });

    // 4) Put it into the container
    branchContainer.appendChild(selectLabel)
    branchContainer.appendChild(selectBranch);

  } catch (err) {
    console.error(err);
    alert(`Failed to load branches: ${err.message}`);
  }
});


// Helper to read a cookie value
function getCookie(name) {
  const cookie = document.cookie
    .split('; ')
    .find(row => row.startsWith(name + '='));
  return cookie ? cookie.split('=')[1] : '';
}



// saving to DB

saveDeviceBtn.addEventListener('click', () => {
    CREATE_DEVICE_URL = "http://localhost:8000/api/v1/devices/"
    // get values
    const serial_number = document.getElementById('serial_number').value;
    const bank = document.getElementById('selectBank').value;
    const branch = document.getElementById('selectBranch').value

    if(!serial_number || !bank ||  !branch){
        throw new Error("Empty Data got.")
    }
    data = {
        serial_number: serial_number,
        branch: branch,
    }
    const res = fetch(
        CREATE_DEVICE_URL,
        {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                //Add csrf_token.
                 'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(data)
        })
        .then((response) => {
            if (!response.ok){
                throw new Error(`HTTP error! Status: ${response.status}`)
            }
            return data.json()
        })
        .then(responseData => console.log(responseData))
        .catch(error => console.error(error))
})