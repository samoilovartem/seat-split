document.addEventListener('DOMContentLoaded', pageLoad)

function pageLoad() {
    loadData()
  }


var data = [{'id': 3, 'account_assigned': 'wdwqd@test.com', 'platform': 'Citi', 'type': 'Virtual', 'parent_card': 'JRL BIZ', 'card_number': '6756453434564534', 'expiration_date': '12/26', 'cvv_number': '124', 'created_by_id': 6, 'team_id': 6, 'created_at': datetime.datetime(2022, 10, 21, 9, 58, 44, 215509, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2022, 10, 21, 10, 41, 23, 100557, tzinfo=datetime.timezone.utc), 'in_tm': True, 'in_tickets_com': True}, {'id': 2, 'account_assigned': 'dwqdwqd@test.com', 'platform': 'Tradeshift', 'type': 'Amex', 'parent_card': 'JRL BIZ', 'card_number': '5567453423453232', 'expiration_date': '10/27', 'cvv_number': '785', 'created_by_id': 1, 'team_id': 6, 'created_at': datetime.datetime(2022, 10, 20, 17, 30, 24, 92981, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2022, 10, 21, 10, 41, 14, 90187, tzinfo=datetime.timezone.utc), 'in_tm': False, 'in_tickets_com': False}, {'id': 1, 'account_assigned': 'PeteGuelli1997@outlook.com', 'platform': 'Tradeshift', 'type': 'Amex', 'parent_card': 'JRL BIZ', 'card_number': '3700218321196952', 'expiration_date': '10/24', 'cvv_number': '887', 'created_by_id': 1, 'team_id': 6, 'created_at': datetime.datetime(2022, 10, 20, 17, 28, 20, 398715, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2022, 10, 21, 10, 41, 32, 999853, tzinfo=datetime.timezone.utc), 'in_tm': False, 'in_tickets_com': False}]

function loadData() {

    var table = new Tabulator("#data-table", {
    height: 500,
    data: data,
    layout: "fitColumns",
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