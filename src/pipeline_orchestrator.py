"""
Mock Pipeline Orchestrator for Frontend Development
NO GPU DEPENDENCIES - Returns realistic dummy data with actual PDF references
"""

import os
import json
import time
import random
import re
from datetime import datetime
from typing import Dict, List, Optional
import yaml

from .summary_generator import MockSummaryGenerator



class MockPipelineOrchestrator:
    """
    Mock orchestrator that simulates pipeline behavior without GPU
    Matches exact structure and methods of real PipelineOrchestrator
    """
    
    def __init__(self, mode: str = "arxiv"):
        """
        Initialize mock orchestrator
        
        Args:
            mode: "arxiv" or "local" - determines which pipeline to use
        """
        print(f"\n{'='*80}")
        print("INITIALIZING MOCK PIPELINE ORCHESTRATOR (NO GPU)")
        print(f"{'='*80}\n")
        
        # Load config
        with open('config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.mode = mode
        self.last_metrics = {}
        
        # Get sample PDFs path
        self.sample_pdfs_path = self.config.get('paths', {}).get('sample_pdfs', 'data/sample_pdfs')
        
        # Load or generate mock paper metadata
        self.mock_papers = self._load_sample_papers()
        
        print("Mock components initialized:")
        print("  ✓ Mock Keyword Extractor")
        print("  ✓ Mock ArXiv Downloader")
        print("  ✓ Mock PDF Processor")
        print("  ✓ Mock Embedding Service")
        print("  ✓ Mock FAISS Indexer")
        print("  ✓ Mock Similarity Search")
        print("  ✓ Mock Reranker")
        print("  ✓ Mock Reasoning Generator")
        print("  ✓ Mock Summary Generator")
        print("  ✓ Mock Local Database Manager")
        
        print(f"\n{'='*80}")
        print(f"[OK] MOCK PIPELINE ORCHESTRATOR READY (Mode: {mode.upper()})")
        print(f"{'='*80}\n")
    
    def _load_sample_papers(self) -> List[Dict]:
        """Load sample PDF metadata from disk or generate if not exist"""
        
        # Check if sample PDFs directory exists
        if not os.path.exists(self.sample_pdfs_path):
            print(f"[INFO] Sample PDFs directory not found: {self.sample_pdfs_path}")
            print(f"[INFO] Using generated mock data without actual PDFs")
            return self._generate_mock_paper_metadata()
        
        # Get list of PDF files (only arXiv format: YYMM.NNNNNvN.pdf)
        pdf_files = [f for f in os.listdir(self.sample_pdfs_path) 
                     if f.endswith('.pdf') and re.match(r'^\d{4}\.\d{5}v\d+\.pdf$', f)]
        
        if not pdf_files:
            print(f"[INFO] No arXiv-format PDF files found in {self.sample_pdfs_path}")
            print(f"[INFO] Expected format: YYMM.NNNNNvN.pdf (e.g., 2201.04337v1.pdf)")
            print(f"[INFO] Using generated mock data")
            return self._generate_mock_paper_metadata()
        
        print(f"[OK] Found {len(pdf_files)} arXiv-format PDFs")
        
        # Generate metadata for actual PDF files
        papers = []
        for i, pdf_file in enumerate(sorted(pdf_files)):  # Sort for consistency
            # Extract arxiv_id from filename
            arxiv_id = self._extract_arxiv_id(pdf_file)
            
            # Generate paper metadata
            paper = {
                'filename': pdf_file,
                'filepath': os.path.join(self.sample_pdfs_path, pdf_file),
                'arxiv_id': arxiv_id,
                'title': self._generate_title_for_paper(pdf_file, i),
                'authors': self._generate_mock_authors(),
                'abstract': self._generate_mock_abstract(i),
                'year': self._extract_year_from_filename(pdf_file),
                'url': f"https://arxiv.org/abs/{arxiv_id}"
            }
            papers.append(paper)
        
        return papers
    
    def _extract_arxiv_id(self, filename: str) -> str:
        """Extract arXiv ID from filename (standard arXiv format only)"""
        # Remove .pdf extension
        name = filename.replace('.pdf', '')
        
        # Standard arXiv format: YYMM.NNNNNvN (e.g., 1803.05449v1)
        # Extract YYMM.NNNNN (remove version suffix)
        if 'v' in name:
            return name.split('v')[0]
        else:
            # Fallback: return as-is if no version suffix
            return name
    
    def _extract_year_from_filename(self, filename: str) -> int:
        """Extract publication year from arXiv filename"""
        name = filename.replace('.pdf', '')
        
        # arXiv format starts with YYMM (e.g., 1803 = 2018 March, 2201 = 2022 January)
        if len(name) >= 4 and name[:2].isdigit():
            year_prefix = int(name[:2])
            
            # Handle year 2000+
            # 91-99 = 1991-1999 (arXiv started in 1991)
            # 00-99 = 2000-2099
            if year_prefix >= 91:
                return 1900 + year_prefix
            else:
                return 2000 + year_prefix
        
        # Fallback
        return 2024
    
    def _generate_title_for_paper(self, filename: str, index: int) -> str:
        """Generate appropriate title based on arXiv ID and index"""
        
        # Diverse title pool mapped to different NLP/ML topics
        titles_pool = [
            # Text Similarity & Embeddings (0-4)
            "SimCSE: Simple Contrastive Learning of Sentence Embeddings",
            "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
            "Improved Deep Metric Learning with Multi-class N-pair Loss Objective",
            "Learning Deep Structured Semantic Models for Web Search",
            "A Simple but Tough-to-Beat Baseline for Sentence Embeddings",
            
            # Retrieval & Search (5-9)
            "Dense Passage Retrieval for Open-Domain Question Answering",
            "ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction",
            "Approximate Nearest Neighbor Negative Contrastive Learning for Dense Text Retrieval",
            "RocketQA: An Optimized Training Approach to Dense Passage Retrieval",
            "ANCE: Learning to Rank with Approximate Nearest Neighbor Negative Contrastive Loss",
            
            # BERT & Transformers (10-14)
            "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
            "RoBERTa: A Robustly Optimized BERT Pretraining Approach",
            "ALBERT: A Lite BERT for Self-supervised Learning of Language Representations",
            "DeBERTa: Decoding-enhanced BERT with Disentangled Attention",
            "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer",
            
            # Neural NLP Methods (15-19)
            "Attention is All You Need",
            "Neural Machine Translation by Jointly Learning to Align and Translate",
            "Convolutional Neural Networks for Sentence Classification",
            "Effective Approaches to Attention-based Neural Machine Translation",
            "GloVe: Global Vectors for Word Representation"
        ]
        
        return titles_pool[index % len(titles_pool)]
    
    def _generate_mock_paper_metadata(self) -> List[Dict]:
        """Generate mock paper metadata when no PDFs available (arXiv format)"""
        papers = []
        
        # Generate 20 papers in standard arXiv format
        base_years = [18, 19, 20, 21, 22, 23, 24, 25]  # 2018-2025
        
        for i in range(20):
            # Generate realistic arXiv ID
            year = base_years[i % len(base_years)]
            month = (i % 12) + 1
            paper_num = 10000 + (i * 1000)
            version = random.randint(1, 4)
            
            arxiv_id = f"{year:02d}{month:02d}.{paper_num:05d}"
            filename = f"{arxiv_id}v{version}.pdf"
            
            paper = {
                'filename': filename,
                'filepath': f"{self.sample_pdfs_path}/{filename}",
                'arxiv_id': arxiv_id,
                'title': self._generate_title_for_paper(filename, i),
                'authors': self._generate_mock_authors(),
                'abstract': self._generate_mock_abstract(i),
                'year': 2000 + year if year < 91 else 1900 + year,
                'url': f"https://arxiv.org/abs/{arxiv_id}"
            }
            papers.append(paper)
        
        return papers
    
    def _generate_mock_authors(self) -> List[str]:
        """Generate mock author names"""
        first_names = ["John", "Maria", "Wei", "Priya", "Ahmed", "Sophie", "Carlos", "Yuki", "Elena", "David", 
                      "Sarah", "Michael", "Lin", "Aisha", "James", "Lucia", "Chen", "Fatima", "Robert", "Ana"]
        last_names = ["Smith", "Garcia", "Wang", "Kumar", "Hassan", "Martin", "Rodriguez", "Tanaka", "Ivanova", "Brown",
                     "Johnson", "Lee", "Chen", "Patel", "Kim", "Silva", "Müller", "Gonzalez", "Wilson", "Anderson"]
        
        num_authors = random.randint(2, 4)
        authors = []
        used_names = set()
        
        for _ in range(num_authors):
            while True:
                first = random.choice(first_names)
                last = random.choice(last_names)
                name = f"{last}, {first[0]}."
                if name not in used_names:
                    used_names.add(name)
                    authors.append(name)
                    break
        
        return authors
    
    def _generate_mock_abstract(self, seed: int) -> str:
        """Generate mock abstract based on seed"""
        random.seed(seed)
        
        templates = [
            f"This paper introduces a novel approach for learning sentence embeddings using contrastive learning objectives. We leverage dropout as a minimal data augmentation technique and show that our method significantly outperforms previous approaches on semantic textual similarity tasks. Our unsupervised SimCSE model achieves {random.randint(75, 85)}% Spearman correlation on STS tasks, while supervised SimCSE reaches {random.randint(82, 88)}%. We demonstrate the effectiveness across seven STS tasks and achieve state-of-the-art performance with simple modifications to existing pre-trained models.",
            
            f"We present a dense passage retrieval system for open-domain question answering that uses dense representations learned through contrastive learning. Unlike traditional sparse retrieval methods based on TF-IDF or BM25, our approach encodes questions and passages into dense vector spaces and retrieves relevant passages via approximate nearest neighbor search. On multiple open-domain QA datasets, our method achieves {random.randint(9, 20)}% absolute improvement in top-20 passage retrieval accuracy over BM25, and shows strong performance when integrated with state-of-the-art reader models.",
            
            f"This work explores pre-training techniques for transformer-based language models. We introduce optimizations including dynamic masking, full sentences without NSP loss, larger mini-batches, and byte-level BPE tokenization. Our approach achieves substantial improvements over BERT on downstream tasks, with particularly strong results on GLUE, RACE, and SQuAD benchmarks. We demonstrate that model architecture choices and training procedures significantly impact performance, achieving {random.randint(85, 92)}% accuracy on challenging language understanding tasks.",
            
            f"We propose a unified framework for natural language processing based on transfer learning from large-scale pre-trained models. Our approach treats every text processing problem as a text-to-text task, where both input and output are text strings. This simple framework allows us to apply the same model, objective, training procedure, and decoding process to diverse tasks including translation, summarization, classification, and question answering. Our model achieves state-of-the-art results on {random.randint(15, 25)} out of {random.randint(20, 30)} benchmarks covering various NLP tasks.",
            
            f"This paper presents an efficient passage retrieval method using contextualized late interaction. Unlike dual-encoder architectures that produce single embedding vectors, our approach maintains token-level representations and performs late interaction using maximum similarity. This design enables more expressive matching while remaining efficient for large-scale search. On MS MARCO passage ranking, our method achieves {random.randint(35, 40)}% MRR@10, surpassing BM25 by over {random.randint(15, 25)}% while maintaining sub-second query latency on millions of passages.",
            
            f"We introduce a self-attention mechanism that scales linearly with sequence length, enabling efficient processing of long documents. Traditional self-attention has quadratic complexity O(n²), limiting applicability to long sequences. Our approach combines local windowed attention with global attention on special tokens, achieving O(n) complexity while maintaining model quality. On long document classification tasks, our method processes sequences up to {random.randint(4, 16)}K tokens and achieves {random.randint(82, 88)}% accuracy, outperforming truncated BERT baselines."
        ]
        
        return random.choice(templates)
    
    def run_pipeline(self, query_abstract: str) -> Optional[Dict]:
        """
        Run the complete pipeline (routes based on mode)
        
        Args:
            query_abstract: Research paper abstract to search for
            
        Returns:
            Dictionary with all results matching real pipeline format
        """
        if self.mode == "local":
            return self.run_local_database_pipeline(query_abstract)
        else:
            return self.run_arxiv_pipeline(query_abstract)
    
    def run_arxiv_pipeline(self, query_abstract: str) -> Optional[Dict]:
        """
        Mock ArXiv pipeline execution
        
        Args:
            query_abstract: Research paper abstract to search for
            
        Returns:
            Dictionary with mock results matching real pipeline format
        """
        pipeline_start = time.time()
        
        print(f"\n{'='*80}")
        print("STARTING MOCK ARXIV PIPELINE")
        print(f"{'='*80}")
        print(f"Query Abstract Length: {len(query_abstract)} characters")
        print(f"Query Word Count: {len(query_abstract.split())} words\n")
        
        try:
            keywords = self._step1_extract_keywords(query_abstract)
            if not keywords:
                return None
            
            arxiv_result = self._step2_search_arxiv(keywords)
            if not arxiv_result or arxiv_result['found'] == 0:
                return None
            
            chunks, doc_metadata = self._step3_build_index(arxiv_result)
            if not chunks:
                return None
            
            top_10_papers = self._step4_search_similar(query_abstract)
            if not top_10_papers:
                return None
            
            top_5_papers = self._step5_rerank(query_abstract, top_10_papers)
            if not top_5_papers:
                return None
            
            comparative_analysis = self._step6_generate_analysis(query_abstract, top_5_papers)
            
            total_time = time.time() - pipeline_start
            self.last_metrics['total_pipeline_time'] = round(total_time, 2)
            
            results = {
                'mode': 'arxiv',
                'query_abstract': query_abstract,
                'query_timestamp': datetime.now().isoformat(),
                'keywords': keywords,
                'arxiv_papers_count': arxiv_result['found'],
                'arxiv_papers': arxiv_result.get('papers', []),
                'chunks_indexed': len(chunks),
                'top_10_papers': top_10_papers,
                'top_5_papers': top_5_papers,
                'comparative_analysis': comparative_analysis,
                'metrics': self.last_metrics,
                'user_confirmed_downloads': arxiv_result.get('user_confirmed', True),
                'files_in_directory': arxiv_result.get('files_in_directory', 0)
            }
            
            self._display_analysis(comparative_analysis)
            self._display_metrics()
            
            output_file = self.save_results(results)
            print(f"\n[OK] Results saved to: {output_file}")
            
            return results
        
        except Exception as e:
            print(f"\n[ERROR] Mock ArXiv pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        finally:
            self._cleanup()
    
    def run_local_database_pipeline(self, query_abstract: str) -> Optional[Dict]:
        """
        Mock Local Database pipeline execution
        
        Args:
            query_abstract: Research paper abstract to search for
            
        Returns:
            Dictionary with mock results matching real pipeline format
        """
        pipeline_start = time.time()
        
        print(f"\n{'='*80}")
        print("STARTING MOCK LOCAL DATABASE PIPELINE")
        print(f"{'='*80}")
        print(f"Query Abstract Length: {len(query_abstract)} characters")
        print(f"Query Word Count: {len(query_abstract.split())} words\n")
        
        try:
            success = self._local_step1_load_or_build_index()
            if not success:
                return None
            
            top_10_papers = self._local_step2_search_similar(query_abstract)
            if not top_10_papers:
                return None
            
            top_5_papers = self._step5_rerank(query_abstract, top_10_papers)
            if not top_5_papers:
                return None
            
            comparative_analysis = self._step6_generate_analysis(query_abstract, top_5_papers)
            
            total_time = time.time() - pipeline_start
            self.last_metrics['total_pipeline_time'] = round(total_time, 2)
            
            results = {
                'mode': 'local_database',
                'query_abstract': query_abstract,
                'query_timestamp': datetime.now().isoformat(),
                'local_database_path': self.config.get('local_database', {}).get('folder_path', 'data/local_database'),
                'total_papers_indexed': len(self.mock_papers),
                'top_10_papers': top_10_papers,
                'top_5_papers': top_5_papers,
                'comparative_analysis': comparative_analysis,
                'metrics': self.last_metrics
            }
            
            self._display_analysis(comparative_analysis)
            self._display_metrics()
            
            output_file = self.save_results(results)
            print(f"\n[OK] Results saved to: {output_file}")
            
            return results
        
        except Exception as e:
            print(f"\n[ERROR] Mock local database pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def load_or_build_local_index(self, force_rebuild: bool = False) -> bool:
        """Mock load or build local index"""
        use_cached = random.choice([True, False]) if not force_rebuild else False
        
        if use_cached:
            print(f"\n{'='*80}")
            print("LOADING CACHED INDEX")
            print(f"{'='*80}\n")
            
            self._simulate_delay(0.3, 0.7)
            self.last_metrics['index_load_time'] = round(random.uniform(0.3, 0.7), 2)
            print(f"[OK] Index loaded successfully ({self.last_metrics['index_load_time']:.2f}s)")
            print(f"{'='*80}\n")
        else:
            print(f"\n{'='*80}")
            print("BUILDING INDEX FROM LOCAL DATABASE")
            print(f"{'='*80}\n")
            
            self._simulate_delay(1.5, 2.5)
            self.last_metrics['index_build_time'] = round(random.uniform(50.0, 90.0), 2)
            print(f"[OK] Index built and cached ({self.last_metrics['index_build_time']:.2f}s)")
            print(f"{'='*80}\n")
        
        return True
    
    def _local_step1_load_or_build_index(self) -> bool:
        """Step 1 for local database: Load or build index"""
        print("STEP 1/4: Loading/Building Local Database Index...")
        
        auto_rebuild = self.config.get('local_database', {}).get('auto_rebuild', False)
        return self.load_or_build_local_index(force_rebuild=auto_rebuild)
    
    def _local_step2_search_similar(self, query_abstract: str) -> Optional[List[Dict]]:
        """Step 2 for local database: Search similar papers"""
        print("\nSTEP 2/4: Searching for Similar Papers in Local Database...")
        
        self._simulate_delay(0.2, 0.4)
        top_10_papers = self._generate_top_10_papers(mode='local')
        self.last_metrics['search_time'] = round(random.uniform(0.08, 0.15), 2)
        
        print(f"[OK] Found {len(top_10_papers)} similar papers")
        self._display_top_10(top_10_papers)
        
        return top_10_papers
    
    def _step1_extract_keywords(self, query_abstract: str) -> Optional[List[str]]:
        """Step 1: Extract keywords from abstract"""
        print("STEP 1/6: Extracting Keywords...")
        
        self._simulate_delay(0.3, 0.6)
        mock_keywords = ["neural networks", "semantic similarity", "deep learning", 
                        "embeddings", "transformers"]
        self.last_metrics['keyword_extraction_time'] = round(random.uniform(0.5, 1.2), 2)
        
        print(f"[OK] Extracted {len(mock_keywords)} keywords")
        return mock_keywords
    
    def _step2_search_arxiv(self, keywords: List[str]) -> Optional[Dict]:
        """Step 2: Search ArXiv and get download links"""
        print("\nSTEP 2/6: Searching ArXiv Papers...")
        print("[INFO] Manual download mode - you will need to download PDFs manually")
        
        self._simulate_delay(0.5, 1.0)
        self.last_metrics['arxiv_search_time'] = round(random.uniform(1.0, 2.5), 2)
        
        arxiv_papers_count = min(20, len(self.mock_papers))
        print(f"[OK] User confirmed - {arxiv_papers_count} PDFs ready")
        
        return {
            'found': arxiv_papers_count,
            'papers': self.mock_papers[:arxiv_papers_count],
            'user_confirmed': True,
            'files_in_directory': arxiv_papers_count,
            'output_dir': self.config.get('paths', {}).get('temp_pdfs', 'data/temp_pdfs')
        }
    
    def _step3_build_index(self, arxiv_result: Dict) -> Optional[tuple]:
        """Step 3: Build FAISS index from PDFs"""
        print("\nSTEP 3/6: Building FAISS Index from PDFs...")
        
        self._simulate_delay(1.0, 1.5)
        chunks_indexed = random.randint(400, 500)
        self.last_metrics['index_build_time'] = round(random.uniform(15.0, 30.0), 2)
        
        print(f"[OK] Found {arxiv_result['files_in_directory']} PDF files in directory")
        print(f"[OK] Generated {chunks_indexed} chunks from PDFs")
        print(f"[OK] FAISS index built successfully")
        
        # Generate mock chunks
        chunks = [f"chunk_{i}" for i in range(chunks_indexed)]
        doc_metadata = {}
        
        return chunks, doc_metadata
    
    def _step4_search_similar(self, query_abstract: str) -> Optional[List[Dict]]:
        """Step 4: Search for similar papers"""
        print("\nSTEP 4/6: Searching for Similar Papers...")
        
        self._simulate_delay(0.2, 0.4)
        top_10_papers = self._generate_top_10_papers(mode='arxiv')
        self.last_metrics['search_time'] = round(random.uniform(0.08, 0.15), 2)
        
        print(f"[OK] Found {len(top_10_papers)} similar papers")
        self._display_top_10(top_10_papers)
        
        return top_10_papers
    
    def _step5_rerank(self, query_abstract: str, top_papers: List[Dict]) -> Optional[List[Dict]]:
        """Step 5: Rerank with Qwen LLM"""
        step_num = "3/4" if self.mode == "local" else "5/6"
        print(f"\nSTEP {step_num}: Reranking with Qwen LLM...")
        
        self._simulate_delay(0.8, 1.2)
        top_5_papers = self._generate_top_5_papers(top_papers)
        self.last_metrics['rerank_time'] = round(random.uniform(3.0, 5.0), 2)
        
        print(f"[OK] Reranked to Top {len(top_5_papers)} papers")
        self._display_top_5(top_5_papers)
        
        return top_5_papers
    
    def _step6_generate_analysis(self, query_abstract: str, top_papers: List[Dict]) -> str:
        """Step 6: Generate comparative analysis"""
        step_num = "4/4" if self.mode == "local" else "6/6"
        print(f"\nSTEP {step_num}: Generating Comparative Analysis...")
        
        self._simulate_delay(1.0, 1.5)
        comparative_analysis = self._generate_mock_analysis(top_papers)
        self.last_metrics['reasoning_time'] = round(random.uniform(4.0, 6.0), 2)
        
        print(f"[OK] Comparative analysis generated")
        
        return comparative_analysis
    
    def _generate_top_10_papers(self, mode: str = 'arxiv') -> List[Dict]:
        """Generate mock top 10 similar papers"""
        top_10 = []
        
        # Select 10 random papers
        num_papers = min(10, len(self.mock_papers))
        selected_papers = random.sample(self.mock_papers, num_papers)
        
        for i, paper in enumerate(selected_papers):
            similarity = round(random.uniform(75.0, 95.0), 1)
            
            # Use appropriate path based on mode
            if mode == 'local':
                pdf_path = paper['filepath'].replace('sample_pdfs', 'local_database')
            else:
                pdf_path = paper['filepath'].replace('sample_pdfs', 'temp_pdfs')
            
            paper_dict = {
                'rank': i + 1,
                'filename': paper['filename'],
                'filepath': pdf_path,
                'local_path': pdf_path if mode == 'local' else None,
                'similarity': similarity,
                'chunk_text': paper['abstract'][:200] + "...",
                'title': paper['title'],
                'authors': paper['authors'],
                'arxiv_id': paper.get('arxiv_id', 'N/A'),
                'year': paper['year'],
                'url': paper.get('url', ''),
                'abstract': paper['abstract']
            }
            
            top_10.append(paper_dict)
        
        # Sort by similarity
        top_10.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Update ranks
        for i, paper in enumerate(top_10):
            paper['rank'] = i + 1
        
        return top_10
    
    def _generate_top_5_papers(self, top_10_papers: List[Dict]) -> List[Dict]:
        """Generate mock top 5 reranked papers"""
        top_5 = []
        
        for i in range(min(5, len(top_10_papers))):
            paper = top_10_papers[i].copy()
            paper['rerank_score'] = round(random.uniform(85.0, 98.0), 1)
            top_5.append(paper)
        
        # Sort by rerank score
        top_5.sort(key=lambda x: x['rerank_score'], reverse=True)
        
        # Update ranks
        for i, paper in enumerate(top_5):
            paper['rank'] = i + 1
        
        return top_5
    
    def _generate_mock_analysis(self, top_5_papers: List[Dict]) -> str:
        """Generate mock comparative analysis"""
        
        analysis = f"""**TOP RECOMMENDED PAPERS**

1. **{top_5_papers[0]['title']}** (Rerank Score: {top_5_papers[0]['rerank_score']})
   - **Relevance**: Directly addresses your query's focus on semantic similarity and neural embedding techniques. The methodology aligns closely with your research objectives.
   - **Key Contribution**: Introduces a novel architecture that achieves state-of-the-art performance on standard benchmarks (STS-B, SICK) with 7-12% improvement over baseline methods.
   - **Research Gap**: While the paper demonstrates strong results on English datasets, scalability to low-resource languages and cross-lingual scenarios remains unexplored. This presents an opportunity for extension.
   - **Technical Highlight**: Uses bidirectional transformers with multi-head attention mechanisms, achieving 95% accuracy with 40% reduced computational cost.

2. **{top_5_papers[1]['title']}** (Rerank Score: {top_5_papers[1]['rerank_score']})
   - **Relevance**: Provides comprehensive coverage of document retrieval systems using transformer-based embeddings, offering valuable insights for implementation strategies.
   - **Key Contribution**: Surveys 50+ retrieval architectures and provides empirical analysis of training strategies, evaluation metrics, and deployment considerations across multiple domains.
   - **Potential Collaboration**: Authors at {random.choice(['Stanford', 'MIT', 'CMU', 'UC Berkeley', 'Google Research'])} have established frameworks that could complement your research direction.
   - **Practical Value**: Includes best practices for real-world deployment, addressing challenges like index size optimization, query latency, and recall-precision trade-offs.

3. **{top_5_papers[2]['title']}** (Rerank Score: {top_5_papers[2]['rerank_score']})
   - **Relevance**: Explores attention mechanisms fundamental to modern NLP systems, providing theoretical foundations applicable to your semantic similarity work.
   - **Key Contribution**: Introduces a novel multi-head attention variant that reduces computational complexity while maintaining performance, relevant for efficient system design.
   - **Future Direction**: Integration of this attention mechanism with your proposed methodology could yield computational efficiency improvements of 30-40%.
   - **Cross-Application**: Demonstrates effectiveness across multiple NLP tasks (translation, summarization, QA), suggesting generalizability to semantic search applications.

**COMPARATIVE ANALYSIS**

The top three papers form a complementary research foundation:
- Paper #1 provides the core methodological framework for semantic similarity
- Paper #2 offers systematic evaluation and deployment strategies
- Paper #3 contributes efficient attention mechanisms for scalability

**Key Synergies:**
- All three emphasize transformer-based architectures with attention mechanisms
- Common focus on balancing performance with computational efficiency
- Shared evaluation on standard benchmarks (STS-B, NQ, TriviaQA)

**Methodological Differences:**
- Paper #1: End-to-end neural approach with contrastive learning
- Paper #2: Survey-based analysis comparing multiple architectures
- Paper #3: Focus on architectural efficiency through attention modifications

**RESEARCH GAPS & OPPORTUNITIES**

1. **Cross-Domain Transfer**: Limited investigation of semantic similarity methods across different scientific domains (medical, legal, technical). Opportunity for domain-adaptive pretraining strategies.

2. **Multilingual Support**: Most approaches focus on English; extending to low-resource languages represents significant research opportunity with practical impact.

3. **Computational Efficiency**: While progress has been made, real-time semantic search on billion-scale document collections requires further optimization, particularly for edge deployment scenarios.

4. **Interpretability**: Current neural methods lack interpretability mechanisms to explain similarity scores, important for scientific applications requiring transparency.

5. **Dynamic Content**: Handling frequently updated document collections without full reindexing remains challenging; incremental learning approaches need investigation.

**RECOMMENDED NEXT STEPS**

1. **Methodological Foundation**: Begin with Paper #1's architecture as baseline, implementing their contrastive learning approach for semantic similarity.

2. **Implementation Guidance**: Use Paper #2's survey findings to inform design decisions around indexing strategy, batch size optimization, and evaluation metrics.

3. **Efficiency Optimization**: Integrate Paper #3's attention mechanism modifications to improve computational efficiency while maintaining accuracy.

4. **Collaboration Opportunities**: Consider reaching out to {random.choice(['Dr. Smith (Stanford)', 'Dr. Chen (MIT)', 'Dr. Johnson (Google Research)', 'Prof. Williams (CMU)'])} whose work on {random.choice(['efficient retrieval', 'cross-lingual embeddings', 'attention mechanisms'])} aligns with your research direction.

5. **Novel Contribution**: Address identified gaps by:
   - Developing domain-adaptive similarity methods for scientific literature
   - Creating multilingual evaluation benchmarks
   - Proposing interpretable similarity scoring mechanisms
   - Designing incremental learning frameworks for dynamic collections

**TECHNICAL RECOMMENDATIONS**

- **Model Architecture**: Dual-encoder or cross-encoder depending on latency requirements (dual-encoder for real-time, cross-encoder for accuracy)
- **Training Strategy**: Contrastive learning with hard negative mining; consider in-batch negatives for efficiency
- **Embedding Dimension**: 768-dim (BERT-base) provides good balance; 384-dim for resource constraints
- **Indexing**: FAISS with IVF for large-scale (>100K docs); Flat index sufficient for smaller collections
- **Evaluation Metrics**: Focus on Recall@K (K=10, 50, 100) and MRR; consider domain-specific metrics for specialized applications"""

        return analysis
    
    def generate_summary(self, paper: Dict) -> Optional[Dict]:
        """
        Generate mock summary for a specific paper
        
        Args:
            paper: Paper dictionary from search results
            
        Returns:
            Mock summary dictionary matching real format
        """        
        mock_summary_gen = MockSummaryGenerator()
        return mock_summary_gen.generate_summary(paper)
    
    def _display_top_10(self, papers: List[Dict]):
        """Display top 10 papers table"""
        print(f"\n{'='*120}")
        print(f"{'Rank':<6} {'Similarity':<12} {'Title':<80}")
        print(f"{'='*120}")
        
        for paper in papers:
            title = paper['title'][:77] + "..." if len(paper['title']) > 77 else paper['title']
            print(f"{paper['rank']:<6} {paper['similarity']:.1f}%{'':<6} {title:<80}")
        
        print(f"{'='*120}")
    
    def _display_top_5(self, papers: List[Dict]):
        """Display top 5 reranked papers"""
        print(f"\n{'='*120}")
        print(f"{'Rank':<6} {'Emb Sim':<10} {'Rerank':<10} {'Title':<80}")
        print(f"{'='*120}")
        
        for paper in papers:
            title = paper['title'][:77] + "..." if len(paper['title']) > 77 else paper['title']
            print(f"{paper['rank']:<6} {paper['similarity']:.1f}%{'':<4} {paper['rerank_score']}/100{'':<4} {title:<80}")
        
        print(f"{'='*120}")
    
    def _display_analysis(self, analysis: str):
        """Display comparative analysis"""
        print(f"\n{'='*80}")
        print("COMPARATIVE ANALYSIS")
        print(f"{'='*80}\n")
        print(analysis)
        print(f"\n{'='*80}")
    
    def _display_metrics(self):
        """Display performance metrics"""
        print(f"\n{'='*80}")
        print("PERFORMANCE METRICS")
        print(f"{'='*80}")
        
        if self.mode == "local":
            if 'index_load_time' in self.last_metrics:
                print(f"Index Load:            {self.last_metrics.get('index_load_time', 0):.2f}s")
            if 'index_build_time' in self.last_metrics:
                print(f"Index Build:           {self.last_metrics.get('index_build_time', 0):.2f}s")
            print(f"Search:                {self.last_metrics.get('search_time', 0):.2f}s")
            print(f"Reranking:             {self.last_metrics.get('rerank_time', 0):.2f}s")
            print(f"Reasoning:             {self.last_metrics.get('reasoning_time', 0):.2f}s")
        else:
            print(f"Keyword Extraction:    {self.last_metrics.get('keyword_extraction_time', 0):.2f}s")
            print(f"ArXiv Search:          {self.last_metrics.get('arxiv_search_time', 0):.2f}s")
            print(f"Index Build:           {self.last_metrics.get('index_build_time', 0):.2f}s")
            print(f"Search:                {self.last_metrics.get('search_time', 0):.2f}s")
            print(f"Reranking:             {self.last_metrics.get('rerank_time', 0):.2f}s")
            print(f"Reasoning:             {self.last_metrics.get('reasoning_time', 0):.2f}s")
        
        print(f"{'-'*80}")
        print(f"Total Pipeline:        {self.last_metrics.get('total_pipeline_time', 0):.2f}s")
        print(f"{'='*80}")
    
    def display_summary(self, summary: Dict):
        """Display paper summary in formatted output"""
        print(f"\n{'='*80}")
        print("PAPER SUMMARY")
        print(f"{'='*80}\n")
        
        print("RESEARCH OBJECTIVE:")
        print(summary.get('research_objective', 'N/A'))
        
        print("\n" + "-"*80)
        print("\nMETHODOLOGY SUMMARY:")
        print(summary.get('methodology_summary', 'N/A'))
        
        print("\n" + "-"*80)
        print("\nKEY FINDINGS:")
        for i, finding in enumerate(summary.get('key_findings', []), 1):
            print(f"{i}. {finding}")
        
        print("\n" + "-"*80)
        print("\nINNOVATION AND CONTRIBUTION:")
        print(summary.get('innovation_and_contribution', 'N/A'))
        
        if summary.get('technical_details'):
            print("\n" + "-"*80)
            print("\nTECHNICAL DETAILS:")
            print(summary.get('technical_details', 'N/A'))
        
        if summary.get('limitations_and_future_work'):
            print("\n" + "-"*80)
            print("\nLIMITATIONS AND FUTURE WORK:")
            print(summary.get('limitations_and_future_work', 'N/A'))
        
        print(f"\n{'='*80}\n")
    
    def save_results(self, results: Dict) -> str:
        """
        Save results to JSON file
        
        Args:
            results: Results dictionary
            
        Returns:
            Path to saved file
        """
        try:
            output_dir = self.config.get('paths', {}).get('output_dir', 'outputs')
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mode_prefix = results.get('mode', 'search')
            output_file = os.path.join(output_dir, f"{mode_prefix}_{timestamp}.json")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            return output_file
        
        except Exception as e:
            print(f"[ERROR] Failed to save results: {e}")
            return "save_failed.json"
    
    def _convert_types(self, obj):
        """Convert numpy types to native Python types for JSON serialization"""
        # Mock version doesn't use numpy, but keep for compatibility
        if isinstance(obj, dict):
            return {key: self._convert_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_types(item) for item in obj]
        return obj
    
    def _cleanup(self):
        """Clean up resources after pipeline execution"""
        try:
            pass
        except Exception as e:
            print(f"[WARNING] Cleanup failed: {e}")
    
    def _simulate_delay(self, min_seconds: float = 0.3, max_seconds: float = 1.0):
        """Simulate processing delay if configured"""
        if self.config.get('mock', {}).get('simulate_delays', True):
            delay = random.uniform(min_seconds, max_seconds)
            time.sleep(delay)


# Testing
if __name__ == "__main__":
    print("Testing Mock Pipeline Orchestrator...\n")
    
    # Test ArXiv mode
    orchestrator = MockPipelineOrchestrator(mode="arxiv")
    
    test_query = """
    We propose a novel deep learning approach for semantic text similarity using 
    BERT embeddings and attention mechanisms. Our method achieves state-of-the-art 
    results on standard benchmarks.
    """
    
    print("\n" + "="*80)
    print("TESTING ARXIV MODE")
    print("="*80)
    
    results = orchestrator.run_pipeline(test_query)
    
    if results:
        print(f"\n✓ Pipeline executed successfully")
        print(f"✓ Found {len(results['top_5_papers'])} top papers")
        print(f"✓ Total time: {results['metrics']['total_pipeline_time']}s")
        
        # Show paper details
        print("\n" + "="*80)
        print("SAMPLE PAPER DETAILS")
        print("="*80)
        sample_paper = results['top_5_papers'][0]
        print(f"Title: {sample_paper['title']}")
        print(f"ArXiv ID: {sample_paper['arxiv_id']}")
        print(f"Filepath: {sample_paper['filepath']}")
        print(f"Year: {sample_paper['year']}")
        
        # Test summary generation
        print("\n" + "="*80)
        print("TESTING SUMMARY GENERATION")
        print("="*80)
        summary = orchestrator.generate_summary(results['top_5_papers'][0])
        if summary:
            print("\n✓ Summary generated successfully")
            orchestrator.display_summary(summary)
    
    # Test Local Database mode
    print("\n\n" + "="*80)
    print("TESTING LOCAL DATABASE MODE")
    print("="*80)
    
    orchestrator_local = MockPipelineOrchestrator(mode="local")
    results_local = orchestrator_local.run_pipeline(test_query)
    
    if results_local:
        print(f"\n✓ Pipeline executed successfully")
        print(f"✓ Found {len(results_local['top_5_papers'])} top papers")
        print(f"✓ Total time: {results_local['metrics']['total_pipeline_time']}s")
    
    print("\n" + "="*80)
    print("MOCK PIPELINE ORCHESTRATOR TESTS COMPLETED")
    print("="*80)