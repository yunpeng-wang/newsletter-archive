const posts = document.querySelector("main #posts");
const maxPerPage = 10;

const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");
const pagerText = document.querySelector("#control span");
const tagsPanel = document.getElementById("tags");
const tagsBtn = tagsPanel.querySelectorAll("div");

let filteredData;
let totalArticle;
let totalPages;
let currentPage = 1;
let currentTag = "All";

function updateMain() {
  posts.innerHTML = "";
  content = "";

  startIdx = (currentPage - 1) * maxPerPage;
  endIdx = startIdx + maxPerPage;

  for (n = startIdx; n < endIdx; n++) {
    if (n < totalArticles) {
      content += filteredData[n];
    }
  }

  posts.innerHTML = content;
  pagerText.innerHTML = String(currentPage) + "/" + String(totalPages);
}

function filterData() {
  if (currentTag == "Levine") {
    filteredData = articleData.filter((item) => item.includes("Levine"));
  } else if (currentTag == "Authers") {
    filteredData = articleData.filter((item) => item.includes("Authers"));
  } else {
    filteredData = articleData;
  }

  totalArticles = filteredData.length;
  totalPages = Math.ceil(totalArticles / maxPerPage);
}

prevBtn.addEventListener("click", () => {
  if (currentPage > 1) {
    currentPage -= 1;
    updateMain();
  }
});

nextBtn.addEventListener("click", () => {
  if (currentPage < totalPages) {
    currentPage += 1;
    updateMain();
  }
});

tagsBtn.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (!btn.classList.contains("active")) {
      let selectTag = btn.dataset.name;
      tagsPanel
        .querySelector(`div[data-name="${currentTag}"]`)
        .classList.toggle("active");
      currentTag = selectTag;
      tagsPanel
        .querySelector(`div[data-name="${currentTag}"]`)
        .classList.toggle("active");

      currentPage = 1;
      filterData();
      updateMain();
    }
  });
});

filterData();
updateMain();
