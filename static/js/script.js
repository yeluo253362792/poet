document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const poemInput = document.getElementById('poem-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultSection = document.getElementById('result-section');
    const languageSelect = document.getElementById('language-select');
    const loader = document.getElementById('loader');
    const resultContent = document.getElementById('result-content');
    const scoreElement = document.getElementById('score');
    const famousSection = document.getElementById('famous-section');
    const originalSection = document.getElementById('original-section');
    const authorElement = document.getElementById('author');
    const creationTimeElement = document.getElementById('creation-time');
    const backgroundElement = document.getElementById('background');
    const stateOfMindElement = document.getElementById('state-of-mind');
    const appreciationElement = document.getElementById('appreciation');

    // Event Listeners
    analyzeBtn.addEventListener('click', analyzePoem);

    // Functions
    async function analyzePoem() {
        const poem = poemInput.value.trim();
        
        if (!poem) {
            alert('请输入诗歌内容');
            return;
        }
        
        // Show result section and loader
        resultSection.classList.add('active');
        resultSection.style.display = 'block';
        loader.style.display = 'block';
        resultContent.style.display = 'none';
        
        try {
            const language = languageSelect.value;
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    poem,
                    language 
                })
            });
            
            if (!response.ok) {
                const errorMsg = languageSelect.value === 'english' ? 'Analysis request failed' : '分析请求失败';
                throw new Error(errorMsg);
            }
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            displayResults(data.analysis);
            
        } catch (error) {
            const errorPrefix = languageSelect.value === 'english' ? 'Error: ' : '错误: ';
            alert(`${errorPrefix}${error.message}`);
            resultSection.style.display = 'none';
        } finally {
            loader.style.display = 'none';
            resultContent.style.display = 'flex';
        }
    }
    
    function displayResults(analysisData) {
        // Parse the JSON response if it's a string
        let analysis;
        try {
            analysis = typeof analysisData === 'string' ? JSON.parse(analysisData) : analysisData;
        } catch (e) {
            // If parsing fails, try to extract JSON from the string (in case the model wrapped it in text)
            try {
                const jsonMatch = analysisData.match(/\{[\s\S]*\}/);
                if (jsonMatch) {
                    analysis = JSON.parse(jsonMatch[0]);
                } else {
                    const errorMsg = languageSelect.value === 'english' ? 'Unable to parse analysis results' : '无法解析分析结果';
                    throw new Error(errorMsg);
                }
            } catch (err) {
                console.error(languageSelect.value === 'english' ? 'Failed to parse analysis results:' : '解析分析结果失败:', err);
                alert(languageSelect.value === 'english' ? 'Unable to parse analysis results, please try again' : '无法解析分析结果，请重试');
                return;
            }
        }
        
        // Update score
        scoreElement.textContent = analysis.score || '--';
        
        // Show/hide sections based on whether the poem is famous
        if (analysis.is_famous) {
            famousSection.style.display = 'block';
            originalSection.style.display = 'none';
            
            // Update famous poem details
            authorElement.textContent = analysis.author || '--';
            creationTimeElement.textContent = analysis.creation_time || '--';
            // 使用marked解析可能包含Markdown的内容
            backgroundElement.innerHTML = analysis.background ? marked.parse(analysis.background) : '--';
        } else {
            famousSection.style.display = 'none';
            originalSection.style.display = 'block';
            
            // Update original poem details
            // 使用marked解析可能包含Markdown的内容
            stateOfMindElement.innerHTML = analysis.state_of_mind ? marked.parse(analysis.state_of_mind) : '--';
        }
        
        // Update appreciation
        // 使用marked解析可能包含Markdown的内容
        appreciationElement.innerHTML = analysis.appreciation ? marked.parse(analysis.appreciation) : '--';
    }
});
