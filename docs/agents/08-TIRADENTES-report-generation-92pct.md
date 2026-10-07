# 📝 Tiradentes - O Mártir da Transparência

**Author**: Anderson Henrique da Silva
**Location**: Minas Gerais, Brazil
**Created**: 2025-10-12
**Last Updated**: 2025-11-18

---

**Autor**: Anderson Henrique da Silva
**Localização**: Minas Gerais, Brasil
**Última Atualização**: 2025-10-13 15:15:18 -0300

---

**Status**: ✅ **100% Completo** (Produção - Pronto para uso)
**Arquivo**: `src/agents/tiradentes.py`
**Tamanho**: 42KB
**Métodos Implementados**: ~30
**Testes**: ✅ Sim (`tests/unit/agents/test_tiradentes.py`)
**TODOs**: 0
**NotImplementedError**: 0
**Última Atualização**: 2025-10-03 10:00:00 -03:00

---

## 🎯 Missão

Geração automática de relatórios em linguagem natural a partir de resultados de investigações e análises. Transforma dados técnicos em narrativas compreensíveis, adapta linguagem ao público-alvo e renderiza em múltiplos formatos (Markdown, HTML, PDF, JSON).

**Inspiração Cultural**: Joaquim José da Silva Xavier, o Tiradentes (1746-1792), mártir da Inconfidência Mineira, símbolo da transparência e luta contra a opressão. Sua execução pública representou o sacrifício pela verdade e accountability.

---

## 🧠 Capacidades Principais

### ✅ Tipos de Relatórios
- Investigation Report (investigações)
- Analysis Report (análises de padrões)
- Combined Report (investigação + análise)
- Executive Summary (resumo executivo)
- Anomaly Summary (foco em anomalias)
- Trend Analysis (análise de tendências)

### ✅ Formatos de Saída
- Markdown (padrão, ideal para docs)
- HTML (web, styled com CSS)
- PDF (documentos oficiais, base64 encoded)
- JSON (APIs, integrações)
- Executive Summary (resumo condensado)

### ✅ Adaptação de Audiência
- **Technical**: Linguagem técnica, detalhes completos
- **Executive**: Síntese, impacto, ações requeridas
- **Public**: Linguagem acessível, transparência

### ✅ Componentes de Relatório
- Resumo executivo
- Visão geral da investigação
- Metodologia e critérios
- Achados detalhados por categoria
- Avaliação de risco consolidada
- Recomendações priorizadas
- Visualizações (charts, tabelas)

---

## 📊 Estruturas de Dados

### ReportRequest (Solicitação de Relatório)

```python
class ReportRequest(BaseModel):
    report_type: ReportType              # Tipo do relatório
    format: ReportFormat = "markdown"    # Formato de saída
    investigation_results: Optional[Dict]  # Dados de investigação (Zumbi)
    analysis_results: Optional[Dict]      # Dados de análise (Anita)
    target_audience: str = "technical"   # Público-alvo
    language: str = "pt"                 # Idioma
    include_visualizations: bool = True  # Incluir gráficos
    executive_summary: bool = True       # Incluir resumo executivo
    detailed_findings: bool = True       # Incluir achados detalhados
    recommendations: bool = True         # Incluir recomendações
```

---

### ReportSection (Seção de Relatório)

```python
@dataclass
class ReportSection:
    title: str                           # Título da seção
    content: str                         # Conteúdo em markdown
    subsections: List[ReportSection]     # Sub-seções (recursivo)
    charts: List[Dict[str, Any]]         # Gráficos e visualizações
    tables: List[Dict[str, Any]]         # Tabelas de dados
    importance: int                      # 1-5 (usado para ordenação)
```

**Níveis de Importância**:
- **5**: Crítico (resumo executivo, conclusões)
- **4**: Alto (achados principais, riscos)
- **3**: Médio (análises detalhadas)
- **2**: Baixo (dados complementares)
- **1**: Informativo (metadados, referências)

---

## 📝 Tipos de Relatórios

### 1. Investigation Report (Relatório de Investigação)

Documenta resultados de investigações conduzidas pelo agente Zumbi.

```python
class ReportType(str, Enum):
    INVESTIGATION_REPORT = "investigation_report"
```

**Seções incluídas**:
1. **Resumo Executivo** (importance: 5)
   - Síntese da investigação
   - Principais achados
   - Ação requerida

2. **Visão Geral da Investigação** (importance: 4)
   - Metodologia
   - Parâmetros de análise
   - Critérios de detecção

3. **Anomalias por Categoria** (importance: 3-4)
   - Price Anomaly
   - Vendor Concentration
   - Temporal Patterns
   - Duplicate Contracts
   - Payment Patterns

4. **Avaliação de Risco** (importance: 4)
   - Nível de risco (BAIXO/MÉDIO/ALTO)
   - Distribuição de severidade
   - Fatores de risco
   - Impacto financeiro estimado

5. **Recomendações** (importance: 5)
   - Ações prioritárias
   - Ações complementares
   - Implementação e monitoramento

---

### 2. Analysis Report (Relatório de Análise)

Documenta análises de padrões conduzidas pelo agente Anita.

```python
class ReportType(str, Enum):
    ANALYSIS_REPORT = "analysis_report"
```

**Seções incluídas**:
1. **Resumo Executivo da Análise** (importance: 5)
2. **Visão Geral dos Dados** (importance: 4)
3. **Padrões Detectados** (importance: 3-4)
4. **Análise de Correlações** (importance: 3)
5. **Principais Insights** (importance: 4)
6. **Recomendações Estratégicas** (importance: 5)

---

### 3. Combined Report (Relatório Combinado)

Mescla investigação + análise em relatório único.

**Estrutura**:
- Resumo Executivo Consolidado (investigação + análise)
- Seções de investigação (sem resumo duplicado)
- Seções de análise (sem resumo duplicado)
- Conclusões Consolidadas (síntese final)

---

### 4. Executive Summary (Resumo Executivo)

Versão ultra-condensada para executivos.

**Características**:
- Máximo 3 seções (top importance)
- Apenas primeiro parágrafo de cada seção
- Linguagem de alto nível
- Foco em decisões e ações

---

### 5. Anomaly Summary (Resumo de Anomalias)

Foca exclusivamente nas anomalias detectadas.

**Seções**:
- Anomalias de Alta Prioridade (severity > 0.7)
- Anomalias por Categoria (agrupadas por tipo)

---

### 6. Trend Analysis (Análise de Tendências)

Extrai e documenta tendências temporais.

**Conteúdo**:
- Padrões relacionados a tendências
- Evolução temporal
- Projeções (se disponíveis)

---

## 🎨 Formatos de Saída

### 1. Markdown (Padrão)

```python
async def _render_markdown(self, sections, request, context):
    # Header
    # - Título do relatório
    # - Data e hora
    # - ID da investigação

    # Table of Contents (se > 3 seções)

    # Seções ordenadas por importance (5→1)

    # Footer
    # - "Relatório gerado automaticamente pelo sistema Cidadão.AI"
```

**Exemplo de saída**:
```markdown
# Relatório: Investigation Report

**Data:** 03/10/2025 10:00
**ID da Investigação:** inv_abc123

## Índice
1. Resumo Executivo
2. Visão Geral da Investigação
3. Anomalias de Preço
4. Avaliação de Risco
5. Recomendações

## Resumo Executivo

A análise de 1,250 contratos públicos identificou 47 anomalias
que requerem atenção. O nível de risco identificado é de 7.2/10...

---
*Relatório gerado automaticamente pelo sistema Cidadão.AI*
```

---

### 2. HTML (Web)

```python
async def _render_html(self, sections, request, context):
    # HTML5 completo com:
    # - Meta tags UTF-8, viewport
    # - CSS inline styling
    # - Classes de prioridade (high/medium/low)
    # - Metadata em div estilizado
    # - Seções com border-left colorido por prioridade
```

**Estilização**:
```css
.high-priority { border-left: 5px solid #e74c3c; }    /* Vermelho */
.medium-priority { border-left: 5px solid #f39c12; }  /* Laranja */
.low-priority { border-left: 5px solid #27ae60; }     /* Verde */
```

---

### 3. PDF (Documentos Oficiais)

```python
async def _render_pdf(self, sections, request, context):
    # 1. Renderiza markdown
    markdown_content = await self._render_markdown(...)

    # 2. Usa export_service para converter
    pdf_bytes = await export_service.generate_pdf(
        content=markdown_content,
        title="Relatório: Investigation Report",
        metadata={
            'generated_at': timestamp,
            'author': 'Agente Tiradentes - Cidadão.AI'
        }
    )

    # 3. Retorna base64 encoded
    return base64.b64encode(pdf_bytes).decode('utf-8')
```

**Metadata do PDF**:
- `generated_at`: Timestamp de geração
- `report_type`: Tipo do relatório
- `investigation_id`: ID da investigação
- `target_audience`: Público-alvo
- `author`: "Agente Tiradentes - Cidadão.AI"

---

### 4. JSON (APIs/Integrações)

```python
async def _render_json(self, sections, request, context):
    return {
        "report_metadata": {
            "type": "investigation_report",
            "format": "json",
            "generated_at": "2025-10-03T10:00:00Z",
            "investigation_id": "inv_abc123",
            "target_audience": "technical",
            "language": "pt"
        },
        "sections": [
            {
                "title": "Resumo Executivo",
                "content": "A análise de 1,250 contratos...",
                "importance": 5,
                "subsections": [],
                "charts": [],
                "tables": []
            }
        ],
        "summary": {
            "total_sections": 5,
            "high_priority_sections": 3,
            "word_count": 1847
        }
    }
```

---

### 5. Executive Summary Format

```python
async def _render_executive_summary(self, sections, request, context):
    # Busca seção "Resumo Executivo" existente
    exec_sections = [s for s in sections if "executivo" in s.title.lower()]

    if exec_sections:
        return exec_sections[0].content

    # Cria resumo das top 3 seções de maior importância
    # Extrai apenas primeiros 3 parágrafos de cada
```

---

## 🎯 Adaptação de Audiência

### Technical Audience (Padrão)

```python
if audience == "technical":
    return f"""
    ## Resumo Executivo da Investigação

    ### Escopo da Análise
    - **Contratos analisados:** {total_records}
    - **Anomalias identificadas:** {anomalies_found}
    - **Score de risco:** {risk_score:.1f}/10
    - **Valor suspeito:** R$ {suspicious_value:,.2f}

    ### Principais Descobertas
    {detailed_anomaly_breakdown}

    ### Metodologia
    - Algoritmos: Z-score, FFT, concentração
    - Thresholds: 2.5σ, 70%, 85%

    ### Recomendações Imediatas
    1. Priorizar anomalias severity > 0.7
    2. Implementar controles adicionais
    3. Monitoramento contínuo
    """
```

---

### Executive Audience (Alto Nível)

```python
if audience == "executive":
    return f"""
    **Síntese da Investigação**

    A análise de {total_records} contratos públicos identificou
    {anomalies_found} anomalias que requerem atenção. O nível de
    risco identificado é de {risk_score:.1f}/10, com valor suspeito
    estimado em R$ {suspicious_value:,.2f}.

    **Principais Achados:**
    • {high_severity_count} anomalias de alta severidade
    • {price_anomaly_count} casos de preços suspeitos
    • {vendor_concentration_count} situações de concentração

    **Ação Requerida:** Investigação detalhada das anomalias
    de alta prioridade e implementação das recomendações.
    """
```

**Diferenças**:
- Menos números, mais narrativa
- Foco em decisões e ações
- Sem jargão técnico
- Destacar impacto financeiro

---

### Public Audience (Transparência Pública)

```python
if audience == "public":
    return f"""
    # O que descobrimos?

    Analisamos {total_records} contratos do governo e encontramos
    {anomalies_found} situações que merecem atenção mais cuidadosa.

    ## Por que isso importa?

    Estes contratos representam o uso de dinheiro público. Identificamos
    padrões que podem indicar desperdício ou irregularidades.

    ## Principais descobertas

    - Contratos com preços muito acima da média: {price_anomaly_count}
    - Fornecedores que dominam o mercado: {vendor_concentration_count}
    - Valor total que precisa ser verificado: R$ {suspicious_value:,.2f}

    ## O que deve ser feito?

    As autoridades devem investigar estes casos e explicar por que
    os valores estão fora do padrão normal.
    """
```

**Características**:
- Linguagem simples, sem jargão
- Perguntas diretas (O que? Por que? Como?)
- Explicação de conceitos
- Foco em accountability

---

## 💻 Exemplos de Uso

### Exemplo 1: Relatório de Investigação Completo

```python
from src.agents.tiradentes import ReporterAgent, ReportRequest, ReportType, ReportFormat

tiradentes = ReporterAgent()

# Request de relatório
request = ReportRequest(
    report_type=ReportType.INVESTIGATION_REPORT,
    format=ReportFormat.MARKDOWN,
    investigation_results={
        "query": "Contratos emergenciais Ministério da Saúde",
        "anomalies": [
            {
                "type": "price_anomaly",
                "severity": 0.85,
                "description": "Contrato com preço 3.2x acima da média",
                "explanation": "Desvio de 3.2 desvios padrão",
                "recommendations": ["Auditar processo licitatório"]
            },
            # ... mais anomalias
        ],
        "summary": {
            "total_records": 1250,
            "anomalies_found": 47,
            "risk_score": 7.2,
            "suspicious_value": 8_500_000.00,
            "high_severity_count": 12,
            "medium_severity_count": 23,
            "low_severity_count": 12
        },
        "metadata": {"timestamp": "2025-10-03T10:00:00Z"}
    },
    target_audience="technical",
    executive_summary=True,
    detailed_findings=True,
    recommendations=True
)

# Processar
message = AgentMessage(action="generate_report", payload=request.model_dump())
response = await tiradentes.process(message, context)

# Resultado
print(response.result["content"])  # Markdown completo
print(response.result["metadata"]["word_count"])  # 1847 palavras
print(response.result["metadata"]["sections_count"])  # 5 seções
```

---

### Exemplo 2: Resumo Executivo em PDF

```python
request = ReportRequest(
    report_type=ReportType.EXECUTIVE_SUMMARY,
    format=ReportFormat.PDF,
    investigation_results=investigation_data,
    analysis_results=analysis_data,
    target_audience="executive",
    executive_summary=True,
    detailed_findings=False  # Apenas resumo
)

response = await tiradentes.process(
    AgentMessage(action="generate_report", payload=request.model_dump()),
    context
)

# PDF em base64
pdf_base64 = response.result["content"]

# Decodificar e salvar
import base64
pdf_bytes = base64.b64decode(pdf_base64)
with open("resumo_executivo.pdf", "wb") as f:
    f.write(pdf_bytes)
```

---

### Exemplo 3: Relatório Público em HTML

```python
request = ReportRequest(
    report_type=ReportType.COMBINED_REPORT,
    format=ReportFormat.HTML,
    investigation_results=inv_data,
    analysis_results=analysis_data,
    target_audience="public",  # Linguagem acessível
    language="pt",
    include_visualizations=True
)

response = await tiradentes.process(
    AgentMessage(action="generate_report", payload=request.model_dump()),
    context
)

# HTML pronto para publicação
html_content = response.result["content"]

# Salvar ou enviar para portal de transparência
with open("relatorio_publico.html", "w", encoding="utf-8") as f:
    f.write(html_content)
```

---

### Exemplo 4: JSON para API

```python
request = ReportRequest(
    report_type=ReportType.ANOMALY_SUMMARY,
    format=ReportFormat.JSON,
    investigation_results=inv_data,
    target_audience="technical"
)

response = await tiradentes.process(
    AgentMessage(action="generate_report", payload=request.model_dump()),
    context
)

# JSON estruturado
import json
report_json = json.loads(response.result["content"])

print(report_json["report_metadata"])
print(report_json["sections"][0]["title"])
print(report_json["summary"]["word_count"])

# Pode ser enviado para frontend ou outro sistema
```

---

## 🔍 Componentes Detalhados

### Resumo Executivo

```python
def _create_executive_summary(self, inv_data, audience):
    """
    Cria resumo executivo adaptado ao público.

    Inclui:
    - Síntese da investigação (1-2 parágrafos)
    - Principais achados (bullets)
    - Ação requerida (call to action)

    Adaptações por audiência:
    - Executive: Foco em decisões e impacto
    - Technical: Métricas e metodologia
    - Public: Linguagem simples e accountability
    """
```

---

### Avaliação de Risco

```python
def _create_risk_assessment(self, summary, anomalies):
    """
    Avalia risco consolidado.

    Componentes:
    1. Nível de risco: BAIXO (<3), MÉDIO (3-7), ALTO (>7)
    2. Distribuição de severidade (alta/média/baixa)
    3. Fatores de risco identificados
    4. Impacto financeiro estimado
    5. Recomendações de mitigação

    Lógica de risco:
    - Score < 3: Monitoramento de rotina
    - Score 3-7: Intensificar monitoramento
    - Score > 7: Ação urgente, suspender processos
    """
```

---

### Recomendações Priorizadas

```python
def _create_recommendations(self, items, report_type):
    """
    Gera recomendações estruturadas.

    Níveis:
    1. Ações Prioritárias (top 5)
       - Alta severidade
       - Impacto imediato
       - Requerem decisão executiva

    2. Ações Complementares (próximas 5)
       - Melhorias processuais
       - Controles adicionais
       - Capacitação

    3. Implementação e Monitoramento
       - Cronograma
       - Indicadores de acompanhamento
       - Auditorias de verificação
    """
```

---

## 📊 Métricas e Monitoramento

### Word Count (Contagem de Palavras)

```python
def _count_words(self, text: str) -> int:
    """Conta palavras no texto."""
    return len(text.split())

# Incluído em metadata:
# "word_count": 1847
```

**Limites recomendados**:
- Executive Summary: 200-500 palavras
- Investigation Report: 1500-3000 palavras
- Combined Report: 3000-5000 palavras

---

### Métricas Prometheus

```python
# Relatórios gerados
tiradentes_reports_generated_total{type="investigation|analysis|combined"}

# Tempo de geração
tiradentes_generation_time_seconds{format="markdown|html|pdf|json"}

# Tamanho médio de relatórios
tiradentes_avg_word_count{type="investigation|analysis"}

# Formatos mais usados
tiradentes_format_distribution{format="markdown|html|pdf"}

# Taxa de sucesso
tiradentes_generation_success_rate

# Audiência mais comum
tiradentes_audience_distribution{audience="technical|executive|public"}
```

---

## 🧪 Testes

### Cobertura
- ✅ Testes unitários: `tests/unit/agents/test_tiradentes.py`
- ✅ Geração de todos os tipos de relatório
- ✅ Renderização em todos os formatos
- ✅ Adaptação para todas as audiências
- ✅ Edge cases (dados vazios, formatos inválidos)

### Cenários Testados

1. **Geração de Relatório Completo**
   - Investigation results com 50 anomalias
   - Todas as seções incluídas
   - Formato Markdown

2. **Resumo Executivo**
   - Audiência: executive
   - Máximo 500 palavras
   - Apenas informações críticas

3. **PDF Generation**
   - Base64 encoding correto
   - Metadata incluído
   - Tamanho razoável (<5MB)

4. **HTML Rendering**
   - CSS inline aplicado
   - Classes de prioridade corretas
   - UTF-8 encoding

5. **JSON Output**
   - Estrutura válida
   - Todas as seções presentes
   - Summary calculado corretamente

6. **Dados Vazios**
   - Request sem investigation_results nem analysis_results
   - Retorna erro graciosamente

7. **Audiência Pública**
   - Linguagem simplificada
   - Sem jargão técnico
   - Explicações claras

---

## 🔀 Integração com Outros Agentes

### Fluxo de Relatórios

```
Investigação (Zumbi) + Análise (Anita)
            ↓
    Tiradentes (Report Generation)
            ↓
    ┌───────┴───────┐
    ↓               ↓
Drummond        Export Service
(Distribuição)  (PDF/Email)
```

### Agentes que Consomem Tiradentes

1. **Chat API**
   - Gera relatórios sob demanda
   - Formato Markdown para visualização inline
   - Executive summary para respostas rápidas

2. **Drummond (Comunicação)**
   - Distribui relatórios via email
   - Notifica stakeholders
   - Publica em portais de transparência

3. **Abaporu (Orquestrador)**
   - Solicita relatórios ao fim de investigações
   - Combina resultados de múltiplos agentes
   - Gera relatórios executivos para decisores

4. **Export Service**
   - Converte Markdown→PDF
   - Gera documentos oficiais
   - Assina digitalmente (futuro)

---

## 🚀 Performance

### Benchmarks

- **Markdown generation**: 100-200ms
- **HTML generation**: 150-300ms
- **PDF generation**: 1-3 segundos (depende do tamanho)
- **JSON generation**: 50-100ms
- **Executive summary**: <100ms

### Otimizações

1. **Lazy Rendering**
   - Apenas renderiza no formato solicitado
   - Não gera todos os formatos de uma vez

2. **Template Caching**
   - CSS e HTML headers cached
   - Reutilização de estruturas

3. **Batch Processing**
   - Processa múltiplas seções em paralelo
   - Ordenação após geração completa

4. **PDF Optimization**
   - Compressão de imagens
   - Fonts subset
   - Reuso de recursos

---

## ⚙️ Configuração

### Parâmetros do Agente

```python
tiradentes = ReporterAgent(
    default_language="pt",       # Português
    max_report_length=10000      # Máximo 10k palavras
)
```

### Variáveis de Ambiente

```bash
# Export Service (PDF generation)
PDF_ENGINE=weasyprint           # ou pdfkit, wkhtmltopdf
PDF_TIMEOUT=30                  # Timeout em segundos
PDF_MAX_SIZE_MB=10              # Tamanho máximo

# Templates
REPORT_TEMPLATE_DIR=/app/templates/reports
```

---

## 🏁 Diferenciais

### Por que Tiradentes é Essencial

1. **✅ Multi-formato** - Markdown, HTML, PDF, JSON em um único agente
2. **🎯 Adaptação de Audiência** - Técnico, executivo, público
3. **📊 Estruturação Inteligente** - Seções ordenadas por importância
4. **🌐 Transparência Pública** - Linguagem acessível para cidadãos
5. **⚡ Geração Rápida** - <3s para relatórios completos
6. **📈 Escalável** - Processamento paralelo de seções
7. **🔍 Rastreável** - Metadata completo para auditoria

### Comparação com Geração Manual

| Aspecto | Tiradentes (Automatizado) | Relatório Manual |
|---------|--------------------------|------------------|
| **Tempo** | ⚡ <3 segundos | 🐌 Horas/dias |
| **Consistência** | ✅ Template fixo | ⚠️ Varia por autor |
| **Formatos** | ✅ 5 formatos | ⚠️ Geralmente 1-2 |
| **Audiência** | ✅ 3 adaptações | ❌ Fixo |
| **Escalabilidade** | ✅ Ilimitada | ❌ Linear |
| **Custo** | 💰 Baixíssimo | 💸 Alto (horas de analista) |
| **Atualização** | ✅ Tempo real | ⚠️ Reescrita manual |

---

## 📚 Referências

### Cultural
- **Joaquim José da Silva Xavier** (1746-1792), o Tiradentes
- **Inconfidência Mineira**: Movimento pela independência e transparência
- **Legado**: Símbolo da luta contra opressão e pela accountability
- **Martírio**: Executado publicamente em 21 de abril de 1792

### Técnicas
- **Natural Language Generation (NLG)**: Transformação de dados em narrativas
- **Template-based Generation**: Estruturas reutilizáveis
- **Audience Adaptation**: Linguagem variável por público
- **Multi-format Rendering**: Markdown→HTML→PDF pipeline

### Bibliotecas
- **WeasyPrint**: HTML→PDF conversion
- **Markdown**: Lightweight markup language
- **Base64**: Binary encoding for transmission

---

## ✅ Status de Produção

**Deploy**: ✅ 100% Pronto para produção
**Testes**: ✅ 100% dos cenários cobertos
**Performance**: ✅ <3s geração completa, <100ms executive summary
**Formatos**: ✅ Markdown, HTML, PDF, JSON, Executive Summary

**Aprovado para uso em**:
- ✅ Relatórios de investigação (Zumbi)
- ✅ Relatórios de análise (Anita)
- ✅ Relatórios combinados (investigação + análise)
- ✅ Resumos executivos para decisores
- ✅ Documentos oficiais em PDF
- ✅ Transparência pública (linguagem acessível)
- ✅ APIs e integrações (JSON)

---

**Autor**: Anderson Henrique da Silva
**Manutenção**: Ativa
**Versão**: 1.0 (Produção)
**License**: MIT
