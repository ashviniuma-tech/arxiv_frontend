"""
Mock Summary Generator Module
Generates realistic paper summaries without GPU/LLM
"""

import time
import random
from typing import Dict, Optional
import yaml


class MockSummaryGenerator:
    """
    Generates detailed structured summaries for individual papers (MOCK VERSION)
    """
    
    def __init__(self):
        """Initialize mock summary generator"""
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        self.max_tokens = config['summary']['max_tokens']
        self.temperature = config['summary']['temperature']
        self.include_methodology = config['summary']['include_methodology']
        self.include_limitations = config['summary']['include_limitations']
        
        print("[OK] Mock Summary Generator initialized")
    
    def generate_summary(self, paper: Dict) -> Optional[Dict]:
        """
        Generate detailed summary for a paper (MOCK VERSION)
        
        Args:
            paper: Paper dictionary with 'filepath' or 'local_path'
            
        Returns:
            Dictionary with structured summary sections
        """
        print(f"\n{'='*80}")
        print("GENERATING PAPER SUMMARY (MOCK)")
        print(f"{'='*80}")
        print(f"Paper: {paper['filename']}")
        
        # Get PDF path
        pdf_path = paper.get('filepath') or paper.get('local_path')
        if not pdf_path:
            print("[ERROR] No PDF path found in paper dictionary")
            return None
        
        # Simulate PDF text extraction
        print(f"\nExtracting text from PDF...")
        self._simulate_delay(0.5, 1.0)
        print(f"[OK] Extracted {random.randint(15000, 25000)} characters")
        
        print("\nGenerating summary with Qwen LLM...")
        print("(This may take 30-60 seconds...)\n")
        
        # Simulate LLM generation time
        self._simulate_delay(2.0, 3.0)
        
        # Generate mock summary based on paper info
        try:
            summary = self._generate_mock_summary(paper)
            
            print(f"[OK] Summary generated ({len(summary['full_text'])} chars)")
            
            # Add metadata
            summary['paper_filename'] = paper['filename']
            summary['paper_similarity'] = paper.get('similarity', 0)
            summary['paper_rank'] = paper.get('rank', 0)
            
            return summary
        
        except Exception as e:
            print(f"[ERROR] Summary generation failed: {e}")
            return None
    
    def _generate_mock_summary(self, paper: Dict) -> Dict:
        """Generate realistic mock summary based on paper metadata"""
        
        title = paper.get('title', 'Research Paper')
        arxiv_id = paper.get('arxiv_id', 'unknown')
        year = paper.get('year', 2024)
        
        # Generate research objective
        research_objective = self._generate_research_objective(title)
        
        # Generate methodology
        methodology_summary = self._generate_methodology(title)
        
        # Generate key findings
        key_findings = self._generate_key_findings(title)
        
        # Generate innovation
        innovation_and_contribution = self._generate_innovation(title)
        
        # Generate technical details
        technical_details = self._generate_technical_details(title)
        
        # Generate limitations (if enabled)
        limitations_and_future_work = ""
        if self.include_limitations:
            limitations_and_future_work = self._generate_limitations(title)
        
        # Build full text
        full_text = f"""[RESEARCH_OBJECTIVE]
{research_objective}

[METHODOLOGY_SUMMARY]
{methodology_summary}

[KEY_FINDINGS]
{chr(10).join(f'- {finding}' for finding in key_findings)}

[INNOVATION_AND_CONTRIBUTION]
{innovation_and_contribution}

[TECHNICAL_DETAILS]
{technical_details}
"""
        
        if self.include_limitations:
            full_text += f"""
[LIMITATIONS_AND_FUTURE_WORK]
{limitations_and_future_work}
"""
        
        summary = {
            "research_objective": research_objective,
            "methodology_summary": methodology_summary,
            "key_findings": key_findings,
            "innovation_and_contribution": innovation_and_contribution,
            "technical_details": technical_details,
            "limitations_and_future_work": limitations_and_future_work,
            "full_text": full_text
        }
        
        return summary
    
    def _generate_research_objective(self, title: str) -> str:
        """Generate research objective based on title"""
        
        if 'semantic' in title.lower() or 'similarity' in title.lower():
            return f"This paper addresses the fundamental challenge of computing semantic similarity between text documents in large-scale information retrieval systems. The primary objective is to develop a more accurate and computationally efficient method for measuring semantic relatedness that captures both lexical and contextual information. This research is crucial for improving search engines, recommendation systems, and question-answering applications where understanding meaning beyond keyword matching is essential."
        
        elif 'retrieval' in title.lower() or 'search' in title.lower():
            return f"The research tackles the problem of efficient document retrieval in massive text collections where traditional keyword-based methods fail to capture semantic intent. The main goal is to design a neural retrieval system that balances accuracy with computational efficiency for real-time applications. This work is important because modern information access systems require both high recall and low latency to serve millions of users effectively."
        
        elif 'embedding' in title.lower() or 'representation' in title.lower():
            return f"This work focuses on learning high-quality vector representations of text that preserve semantic relationships in a continuous vector space. The primary objective is to create embeddings that generalize across diverse tasks while remaining computationally tractable for deployment. This research is needed because existing representation learning methods often struggle with domain adaptation and require task-specific fine-tuning."
        
        elif 'bert' in title.lower() or 'transformer' in title.lower():
            return f"The paper investigates effective fine-tuning strategies for pre-trained transformer models on downstream natural language processing tasks. The main research question is how to adapt large language models efficiently without catastrophic forgetting while improving task-specific performance. This research is significant because it addresses the practical challenges of deploying billion-parameter models in resource-constrained production environments."
        
        elif 'contrastive' in title.lower():
            return f"This research explores contrastive learning frameworks for unsupervised representation learning from large unlabeled text corpora. The primary goal is to learn discriminative embeddings that separate semantically different texts while clustering similar ones. This work is important because it reduces dependence on expensive labeled data while achieving competitive performance on various benchmarks."
        
        elif 'cross-lingual' in title.lower() or 'multilingual' in title.lower():
            return f"The paper addresses the challenge of semantic understanding across multiple languages without requiring parallel corpora for each language pair. The main objective is to develop a unified multilingual representation space that enables zero-shot cross-lingual transfer. This research is crucial for democratizing natural language processing technologies for low-resource languages."
        
        else:
            return f"This paper investigates advanced methods for natural language understanding and processing in complex real-world scenarios. The primary objective is to develop robust algorithms that generalize across diverse datasets and domains while maintaining computational efficiency. This research is important for advancing the state-of-the-art in machine learning applications for text analysis."
    
    def _generate_methodology(self, title: str) -> str:
        """Generate methodology summary based on title"""
        
        base = f"The study employs a comprehensive experimental framework combining neural architecture design, large-scale pre-training, and rigorous evaluation protocols. "
        
        if 'bert' in title.lower() or 'transformer' in title.lower():
            return base + f"The methodology centers on fine-tuning a pre-trained BERT-base model with {random.randint(110, 340)} million parameters using a dual-encoder architecture. The training process utilizes contrastive loss with in-batch negatives sampled from batches of {random.choice([32, 64, 128])} examples. The authors collect training data from multiple sources including Wikipedia, BookCorpus, and domain-specific corpora totaling {random.randint(5, 50)} million sentence pairs. Key hyperparameters include a learning rate of {random.choice(['1e-5', '2e-5', '3e-5'])} with linear warmup, batch size of {random.choice([256, 512, 1024])}, and training for {random.randint(3, 10)} epochs. Evaluation is conducted on standard benchmarks including STS-B, SICK-R, and custom test sets using Spearman correlation and accuracy metrics."
        
        elif 'contrastive' in title.lower():
            return base + f"The core approach implements a contrastive learning framework where positive pairs are constructed through data augmentation techniques including dropout masking, back-translation, and paraphrasing. Negative samples are selected using hard negative mining with dynamic difficulty adjustment based on model confidence scores. The architecture employs a siamese network structure with shared encoders and a temperature-scaled cosine similarity objective. Training data comprises {random.randint(10, 100)} million text pairs extracted from diverse sources. Important configurations include temperature parameter τ = {random.choice(['0.05', '0.07', '0.1'])}, embedding dimension of {random.choice([256, 384, 768])}, and {random.randint(6, 12)}-layer transformer encoders. The study conducts ablation experiments to assess the contribution of each component and validates performance across {random.randint(5, 15)} different benchmarks."
        
        elif 'retrieval' in title.lower():
            return base + f"The methodology implements a two-stage retrieval pipeline consisting of an efficient first-pass retrieval using approximate nearest neighbor search followed by neural reranking. The first stage employs FAISS indexing with {random.choice(['IVF', 'HNSW', 'Flat'])} structure over {random.randint(768, 1024)}-dimensional dense vectors. Document collections ranging from {random.randint(100, 1000)}K to {random.randint(1, 10)}M passages are indexed for evaluation. The neural reranker is a cross-encoder model that computes relevance scores for top-{random.randint(50, 200)} candidates from the first stage. Training utilizes the MS MARCO and Natural Questions datasets with {random.randint(100, 500)}K labeled query-document pairs. Key experimental parameters include batch size of {random.choice([16, 32, 64])}, maximum sequence length of {random.choice([256, 512])}, and learning rate scheduling with polynomial decay. Performance is measured using standard information retrieval metrics including MRR@10, Recall@100, and nDCG@10."
        
        elif 'embedding' in title.lower():
            return base + f"The approach develops universal sentence embeddings through multi-task learning across {random.randint(5, 15)} diverse NLP tasks simultaneously. The encoder architecture is based on transformer networks with {random.randint(6, 12)} attention layers and {random.choice([256, 384, 512, 768])}-dimensional hidden states. Training data aggregates {random.randint(50, 500)} million examples from natural language inference, paraphrase detection, semantic similarity, and question answering datasets. The methodology incorporates task-specific projection layers while sharing the core encoder parameters to enable knowledge transfer. Important training configurations include gradient accumulation over {random.choice([2, 4, 8])} steps, mixed-precision training for efficiency, and adaptive learning rate with cosine annealing. The study evaluates embeddings on {random.randint(10, 20)} downstream tasks using linear probing and zero-shot transfer protocols to assess generalization capabilities."
        
        else:
            return base + f"The research implements state-of-the-art neural architectures with {random.randint(100, 500)} million parameters trained on large-scale datasets comprising {random.randint(10, 100)} million samples. The training pipeline incorporates distributed computing across {random.randint(4, 32)} GPUs with data parallelism and gradient checkpointing for memory efficiency. Experiments systematically vary key hyperparameters including learning rate ({random.choice(['1e-5', '5e-5', '1e-4'])}), batch size ({random.choice([64, 128, 256])}), and model depth ({random.randint(6, 24)} layers). The study employs cross-validation with {random.randint(3, 5)}-fold splits and statistical significance testing to ensure robust conclusions. Evaluation encompasses both automatic metrics and human judgments collected from {random.randint(20, 100)} expert annotators to assess quality comprehensively."
    
    def _generate_key_findings(self, title: str) -> list:
        """Generate key findings based on title"""
        
        findings_pool = [
            f"The proposed method achieves {random.randint(85, 95)}.{random.randint(0, 9)}% accuracy on the STS-B benchmark, representing a {random.randint(3, 12)}.{random.randint(0, 9)}% absolute improvement over the previous state-of-the-art baseline.",
            
            f"Experimental results demonstrate that the approach reduces computational latency by {random.randint(30, 60)}% while maintaining comparable performance, enabling deployment in real-time applications with sub-{random.randint(50, 200)}ms response time.",
            
            f"Ablation studies reveal that {random.choice(['contrastive pre-training', 'hard negative mining', 'multi-task learning', 'attention mechanisms'])} contributes {random.randint(15, 40)}% of the overall performance gain, highlighting its critical importance to the system.",
            
            f"Cross-domain evaluation shows robust generalization with performance degradation of only {random.randint(2, 8)}% when transferring from news articles to {random.choice(['scientific papers', 'social media posts', 'legal documents', 'medical records'])}, compared to {random.randint(15, 30)}% for baseline methods.",
            
            f"The model achieves Spearman correlation of {random.uniform(0.80, 0.95):.3f} on semantic similarity tasks and Recall@{random.choice([10, 50, 100])} of {random.randint(75, 95)}% on information retrieval benchmarks, outperforming {random.randint(10, 30)} competing approaches.",
            
            f"Analysis of learned representations reveals that the embedding space naturally clusters semantically related concepts with {random.randint(85, 98)}% intra-cluster coherence and clear separation between distinct topics with inter-cluster distance exceeding {random.uniform(0.6, 0.9):.2f}.",
            
            f"Scaling experiments demonstrate near-linear performance improvements with model size, with {random.choice(['340M', '750M', '1.5B'])} parameter variants achieving {random.randint(5, 15)}% higher scores than {random.choice(['110M', '220M', '340M'])} parameter baselines on complex reasoning tasks.",
            
            f"Zero-shot transfer to {random.randint(5, 20)} unseen domains yields {random.randint(70, 88)}% of supervised performance, validating the generalization capacity and reducing annotation requirements by approximately {random.randint(70, 90)}%.",
            
            f"Efficiency analysis shows that the optimized implementation processes {random.randint(500, 5000)} queries per second on standard hardware, representing a {random.randint(5, 20)}× speedup over previous methods while using {random.randint(30, 60)}% less memory.",
            
            f"Error analysis identifies that {random.randint(60, 80)}% of failure cases involve specialized domain terminology or nuanced semantic distinctions, suggesting directions for targeted improvements in future work."
        ]
        
        # Return 4-5 findings
        num_findings = random.randint(4, 5)
        return random.sample(findings_pool, num_findings)
    
    def _generate_innovation(self, title: str) -> str:
        """Generate innovation and contribution based on title"""
        
        innovations = [
            f"This work introduces a novel {random.choice(['attention mechanism', 'pooling strategy', 'training objective', 'architecture design'])} that addresses fundamental limitations of existing approaches. Unlike previous methods that {random.choice(['rely on expensive labeled data', 'require task-specific fine-tuning', 'suffer from poor generalization', 'have high computational costs'])}, the proposed approach achieves superior performance through {random.choice(['self-supervised pre-training', 'parameter-efficient adaptation', 'multi-task learning', 'contrastive learning'])}. The main contribution is a unified framework that seamlessly integrates {random.choice(['representation learning', 'retrieval', 'ranking', 'classification'])} tasks within a single architecture.",
            
            f"The innovation lies in the combination of {random.choice(['dense retrieval', 'sparse attention', 'cross-encoder reranking', 'hybrid indexing'])} with {random.choice(['transformer-based encoders', 'contrastive objectives', 'meta-learning', 'knowledge distillation'])}, which has not been explored in prior literature. This differs from previous research by explicitly modeling {random.choice(['long-range dependencies', 'hierarchical structure', 'semantic compositionality', 'contextual variations'])} while maintaining computational efficiency. The work contributes three key innovations: (1) a scalable training procedure, (2) an efficient inference algorithm, and (3) extensive empirical validation across diverse benchmarks.",
            
            f"The primary innovation is the development of a {random.choice(['parameter-efficient', 'domain-adaptive', 'language-agnostic', 'task-agnostic'])} framework that achieves state-of-the-art results with significantly reduced resource requirements. Unlike existing approaches that require {random.choice(['billions of parameters', 'millions of labeled examples', 'extensive hyperparameter tuning', 'specialized hardware'])}, this method leverages {random.choice(['transfer learning', 'data augmentation', 'knowledge distillation', 'multi-task learning'])} to achieve comparable performance with {random.randint(50, 90)}% fewer resources. The contribution extends beyond technical improvements to provide practical insights for real-world deployment."
        ]
        
        base_innovation = random.choice(innovations)
        
        impact = f" The potential impact is substantial, as the approach enables {random.choice(['democratization of NLP technologies', 'deployment in low-resource settings', 'real-time processing of massive datasets', 'cross-lingual knowledge transfer'])} and opens new research directions in {random.choice(['few-shot learning', 'domain adaptation', 'efficient transformers', 'neural information retrieval'])}. The advantages over existing approaches include {random.randint(20, 60)}% improved efficiency, better generalization to unseen domains, and simplified training procedures that reduce time-to-deployment from weeks to days."
        
        return base_innovation + impact
    
    def _generate_technical_details(self, title: str) -> str:
        """Generate technical details based on title"""
        
        details = [
            f"The implementation uses {random.choice(['PyTorch', 'TensorFlow', 'JAX'])} {random.choice(['1.12', '1.13', '2.0', '2.1'])} with mixed-precision training (FP16) to accelerate computations. The model architecture consists of {random.randint(6, 24)} transformer layers with {random.randint(8, 16)} attention heads and hidden dimension of {random.choice([256, 384, 512, 768, 1024])}. Training utilizes the AdamW optimizer with weight decay of {random.choice(['0.01', '0.001', '0.0001'])} and gradient clipping at norm {random.choice(['1.0', '5.0', '10.0'])}. The learning rate schedule employs linear warmup for {random.randint(1000, 10000)} steps followed by cosine decay. Batch size is set to {random.choice([32, 64, 128, 256])} with gradient accumulation over {random.choice([2, 4, 8])} steps for effective batch size of {random.choice([256, 512, 1024])}.",
            
            f"Key technical specifications include embedding dimension of {random.choice([256, 384, 512, 768])}, maximum sequence length of {random.choice([128, 256, 512])} tokens, and vocabulary size of {random.choice(['30K', '50K', '100K'])}. The model employs {random.choice(['GELU', 'ReLU', 'SiLU'])} activation functions and {random.choice(['layer normalization', 'batch normalization', 'RMS normalization'])} for stable training. Performance evaluation uses metrics including F1 score, accuracy, Spearman correlation, and {random.choice(['MRR@10', 'nDCG@10', 'Recall@100'])}. Computational requirements involve {random.randint(4, 32)} {random.choice(['V100', 'A100', 'H100'])} GPUs with {random.randint(16, 80)}GB memory each, and training time ranges from {random.randint(12, 72)} hours depending on dataset size.",
            
            f"The system implements efficient attention mechanisms with computational complexity of O(n log n) instead of O(n²) for sequences of length n. Important hyperparameters include dropout rate of {random.choice(['0.1', '0.2', '0.3'])}, temperature parameter of {random.choice(['0.05', '0.07', '0.1'])} for contrastive loss, and margin of {random.choice(['0.2', '0.5', '1.0'])} for triplet loss formulations. The model uses {random.choice(['WordPiece', 'BPE', 'SentencePiece'])} tokenization with {random.choice(['uncased', 'cased'])} vocabulary. Inference optimization includes ONNX export, TensorRT compilation, and quantization to INT8 precision, achieving {random.randint(2, 5)}× speedup with minimal accuracy loss of less than {random.uniform(0.5, 2.0):.1f}%."
        ]
        
        return random.choice(details)
    
    def _generate_limitations(self, title: str) -> str:
        """Generate limitations and future work"""
        
        limitations = [
            f"The authors acknowledge several limitations of the current approach. First, the model's performance degrades on {random.choice(['extremely long documents', 'specialized technical domains', 'low-resource languages', 'noisy social media text'])} that differ significantly from the training distribution. Second, computational requirements remain substantial for training, requiring access to {random.choice(['high-end GPUs', 'distributed computing resources', 'large-scale datasets'])}, which may limit reproducibility. Third, the evaluation primarily focuses on {random.choice(['English language texts', 'news articles', 'academic papers'])}, and generalization to other {random.choice(['languages', 'domains', 'text genres'])} needs further investigation. Future work should explore {random.choice(['parameter-efficient fine-tuning', 'few-shot learning', 'continual learning', 'cross-lingual transfer'])} to address these limitations and extend the approach to {random.choice(['multimodal settings', 'interactive systems', 'real-time applications', 'edge devices'])}.",
            
            f"While the proposed method shows promising results, several constraints merit discussion. The reliance on large pre-training datasets may introduce biases that affect downstream performance on minority groups or specialized applications. The model's interpretability remains limited, making it difficult to diagnose failure modes or provide explanations for predictions. Computational costs during inference, though improved, still exceed requirements for deployment on resource-constrained devices. Future research directions include developing {random.choice(['more efficient architectures', 'better interpretability methods', 'bias mitigation techniques', 'adaptive inference strategies'])}, investigating {random.choice(['zero-shot transfer', 'meta-learning', 'neural architecture search'])}, and extending evaluation to include {random.choice(['fairness metrics', 'robustness testing', 'human evaluations', 'long-term deployment studies'])}.",
            
            f"The study identifies several areas for improvement and extension. Current experiments are limited to datasets with {random.choice(['fewer than 1M examples', 'relatively short texts', 'high-resource languages'])}, and scaling to {random.choice(['billion-scale corpora', 'very long documents', 'hundreds of languages'])} presents both technical and methodological challenges. The approach assumes availability of {random.choice(['clean training data', 'balanced class distributions', 'sufficient computational resources'])}, which may not hold in real-world scenarios. The authors suggest future work should focus on {random.choice(['improving sample efficiency', 'handling noisy labels', 'developing unsupervised methods', 'enabling continual learning'])}, exploring {random.choice(['alternative training objectives', 'novel architectures', 'hybrid approaches'])}, and conducting more comprehensive {random.choice(['ablation studies', 'error analyses', 'human evaluations', 'deployment case studies'])}."
        ]
        
        return random.choice(limitations)
    
    def _simulate_delay(self, min_seconds: float, max_seconds: float):
        """Simulate processing delay"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)


# Standalone testing
if __name__ == "__main__":
    print("Testing Mock Summary Generator...\n")
    
    # Create dummy paper
    dummy_paper = {
        'rank': 1,
        'filename': '2201.04337v2.pdf',
        'filepath': 'data/sample_pdfs/2201.04337v2.pdf',
        'similarity': 95.0,
        'title': 'SimCSE: Simple Contrastive Learning of Sentence Embeddings',
        'arxiv_id': '2201.04337',
        'year': 2022
    }
    
    generator = MockSummaryGenerator()
    
    print("\nGenerating mock summary...")
    summary = generator.generate_summary(dummy_paper)
    
    if summary:
        print("\n" + "="*80)
        print("GENERATED SUMMARY")
        print("="*80)
        print(f"\nResearch Objective:\n{summary['research_objective']}")
        print(f"\nMethodology:\n{summary['methodology_summary']}")
        print(f"\nKey Findings:")
        for i, finding in enumerate(summary['key_findings'], 1):
            print(f"{i}. {finding}")
        print(f"\nInnovation:\n{summary['innovation_and_contribution']}")
        print(f"\nTechnical Details:\n{summary['technical_details']}")
        if summary['limitations_and_future_work']:
            print(f"\nLimitations:\n{summary['limitations_and_future_work']}")
        
        print("\n✓ Mock Summary Generator Test Completed Successfully")
    else:
        print("\n✗ Summary generation failed")