document.addEventListener('DOMContentLoaded', pageLoad)

function pageLoad() {
    loadData()
  }


function loadData() {

    var table = new Tabulator("#data-table", {
    height:500,
    data:{{ data }},
    layout:"fitColumns",
    pagination: true,
    paginationSize: 15,
    columns: [
      {
        title:"Id",
        field:"id"
      },
      {
        title:"Account assigned",
        field:"account_assigned",
        width: 150,
      },
      {
        title:"Platform",
        field:"platform",
        width: 100,
        hozAlign: 'right',
      },
      {
        title:"Type",
        field:"type",
        width: 120,
        hozAlign: 'right',
      },
      {
        title:"Parent card",
        field:"parent_card",
        hozAlign:"center",
      },
      {
        title:"Card number",
        field:"card_number",
        width: 150,
      {
        title:"Expiration date",
        field:"expiration_date",
        width: 80,
      },
      {
        title:"CVV number",
        field:"cvv_number",
      },
      {
        title: 'Created by',
        field: 'created_by_id',
        hozAlign: 'left',
      },
      {
        title: 'Team',
        field: 'team_id',
        width: 140,
        hozAlign: 'center',
      },
      {
        title: 'Added in TM',
        field: 'in_tm',
        width: 140,
        hozAlign: 'center',
      },
      {
        title: 'Added in tickets.com',
        field: 'in_tickets_com',
        width: 140,
        hozAlign: 'center',
      },
    ],
  })
}