document.addEventListener('DOMContentLoaded', function() {
  const productRangeAll = document.querySelector('#id_campaign_targets_0');
  const productRangeSpecific = document.querySelector('#id_campaign_targets_1');
  const filtersDataInput = document.querySelector('#id_filters_data');
  const dslDisplay = document.querySelector('#id_dsl');

  const modalOverlay = document.querySelector('#filter-modal-overlay');
  const popupFiltersContainer = document.querySelector('#popup-filters-container');
  const popupAddFilterBtn = document.querySelector('#popup-add-filter-btn');
  const popupCancelBtn = document.querySelector('#popup-cancel-btn');
  const popupDoneBtn = document.querySelector('#popup-done-btn');

  function createFilterRow() {
    const filterRow = document.createElement('div');
    filterRow.style.marginBottom = '5px';

    const fieldSelect = document.createElement('select');
    ['brand_id','product_id','mov','customer_segment'].forEach(f=>{
      const opt=document.createElement('option');
      opt.value=f; opt.textContent=f;
      fieldSelect.appendChild(opt);
    });

    const opSelect=document.createElement('select');
    ['=','>','<','>=','<=','IN'].forEach(o=>{
      const opt=document.createElement('option');
      opt.value=o; opt.textContent=o;
      opSelect.appendChild(opt);
    });

    const valueInput=document.createElement('input');
    valueInput.type='text';
    valueInput.placeholder='Value or comma-separated list';
    valueInput.className='vTextField';

    const removeBtn=document.createElement('button');
    removeBtn.textContent='x';
    removeBtn.style.marginLeft='5px';
    removeBtn.onclick=()=>filterRow.remove();

    [fieldSelect,opSelect,valueInput,removeBtn].forEach(el=>filterRow.appendChild(el));
    return filterRow;
  }

  popupAddFilterBtn.addEventListener('click', function(e){
    e.preventDefault();
    const row = createFilterRow();
    popupFiltersContainer.appendChild(row);
  });

  popupCancelBtn.addEventListener('click', function(){
    // 취소 시 DSL 비우기
    filtersDataInput.value = '';
    dslDisplay.textContent = '';
    modalOverlay.style.display='none';
  });

  popupDoneBtn.addEventListener('click', function(){
    // 현재 필터들 읽어와 DSL 생성
    const filtersData = [];
    popupFiltersContainer.querySelectorAll('div').forEach(row=>{
      const selects=row.querySelectorAll('select');
      const input=row.querySelector('input');
      const field=selects[0].value;
      const op=selects[1].value;
      const valStr=input.value.trim();
      const val=(op.toUpperCase()==='IN')?valStr.split(',').map(v=>v.trim()):valStr;
      filtersData.push({field:field, operator:op, value:val});
    });

    // filtersDataInput.value = JSON.stringify(filtersData);

    // console.log(filtersDataInput.value);

    // DSL 생성 로직: 간단히 field op val 형태 AND 조합
    let conditions = [];
    for(let f of filtersData) {
      if(f.operator.toUpperCase()==='IN'){
        conditions.push(`${f.field} IN [${f.value.join(',')}]`);
      } else {
        conditions.push(`${f.field} ${f.operator} ${f.value}`);
      }
    }
    let dsl = conditions.length? conditions.join(" AND ") : "";
    dslDisplay.textContent = dsl;

    modalOverlay.style.display='none';
  });

  function toggleModal(show){
    modalOverlay.style.display = show?'block':'none';
  }

  function toggleFilters(){
    if(productRangeAll.checked){
      // all
      filtersDataInput.value='';
      dslDisplay.textContent='';
    } else {
      // specific -> popup
      toggleModal(true);
    }
  }

  productRangeAll.addEventListener('change',toggleFilters);
  productRangeSpecific.addEventListener('change',toggleFilters);

});

function validateFilters() {
  let valid = true;
  popupFiltersContainer.querySelectorAll('div').forEach(row => {
    const selects = row.querySelectorAll('select');
    const input = row.querySelector('input');
    const op = selects[1].value;
    const valStr = input.value.trim();

    // IN이 아닌 경우 ","나 " " 체크
    if (op.toUpperCase() !== 'IN' && (valStr.indexOf(',') !== -1 || valStr.indexOf(' ') !== -1)) {
      valid = false;
      input.style.borderColor = 'red';
    } else {
      input.style.borderColor = '';
    }
  });

  popupDoneBtn.disabled = !valid;
}

popupFiltersContainer.addEventListener('input', validateFilters);
popupFiltersContainer.addEventListener('change', validateFilters);