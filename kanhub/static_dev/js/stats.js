const labels = [
{% for tag in tasks_by_tags %}
"{{ tag.tags__name }}",
{% endfor %}
];

const data = {
labels: labels,
datasets: [{
  label: "Количество задач по тегам",
  data: [
    {% for tag in tasks_by_tags %}
    {{ tag.count }},
    {% endfor %}
  ],
  backgroundColor: [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)'
  ],
  borderColor: [
    'rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)'
  ],
  borderWidth: 1
}]
};

const config = {
type: 'bar',
data: data,
options: {
  scales: {
    y: {
      beginAtZero: true
    }
  },
  responsive: true,
  maintainAspectRatio: false
}
};

const tasksChart = new Chart(
document.getElementById('tasksChart'),
config
);