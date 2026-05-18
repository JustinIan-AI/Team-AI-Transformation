#!/usr/bin/env python3
"""
企业深度调研框架生成器
Enterprise Deep Research Framework Generator

生成结构化的企业调研框架和搜索问题清单，供 AI 智能体通过 web-search 工具或本地文档完成实际调研。
Generates a structured research framework and search queries for AI agents
to conduct actual research via web-search tools or local documents.

输入：公司名称、国家、可选的本地文档目录
输出：结构化调研框架（Markdown / JSON）

版本：1.1.0
"""

__version__ = "1.1.0"

import argparse
import json
import sys
import os
import glob
import datetime
from typing import Dict, List


def log_execution(company_name: str, output_path: str, format_type: str, local_docs_dir: str = None):
    """
    记录执行日志
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": __version__,
        "company_name": company_name,
        "output_path": output_path,
        "format": format_type,
        "local_docs_dir": local_docs_dir,
        "status": "success"
    }
    
    log_file = os.path.join(log_dir, f"execution_{datetime.date.today().strftime('%Y%m%d')}.log")
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    print(f"[日志] 执行记录已保存到: {log_file}")


class CompanyResearcher:
    """企业调研框架生成器"""

    def __init__(self, company_name: str, country: str = "中国", local_docs_dir: str = None):
        self.company_name = company_name
        self.country = country
        self.local_docs_dir = local_docs_dir
        self.local_docs_content = {}

    def _load_local_docs(self) -> None:
        """
        加载本地 Markdown 文档内容
        """
        if not self.local_docs_dir or not os.path.isdir(self.local_docs_dir):
            return

        print(f"[调研] 正在加载本地文档目录: {self.local_docs_dir}")
        md_files = glob.glob(os.path.join(self.local_docs_dir, "**/*.md"), recursive=True)
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_name = os.path.basename(md_file)
                    self.local_docs_content[file_name] = content
                    print(f"[调研] 已加载: {file_name}")
            except Exception as e:
                print(f"[警告] 无法读取文件 {md_file}: {e}", file=sys.stderr)

    def _extract_info_from_local_docs(self, keyword: str) -> str:
        """
        从本地文档中提取指定关键词的信息
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            str: 提取到的信息
        """
        results = []
        for file_name, content in self.local_docs_content.items():
            if keyword in content:
                # 提取关键词附近的上下文（前后各5行）
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if keyword in line:
                        start = max(0, i - 5)
                        end = min(len(lines), i + 6)
                        context = '\n'.join(lines[start:end])
                        results.append(f"【{file_name}】\n{context}")
        
        return '\n\n'.join(results) if results else "未找到相关信息"

    def research_company(self) -> Dict:
        """
        生成企业调研框架

        Returns:
            Dict: 包含调研框架和搜索问题清单的字典
        """
        print(f"[调研] 正在生成 {self.company_name} 的调研框架...")
        
        # 加载本地文档（如果指定了目录）
        self._load_local_docs()
        
        return self._generate_company_framework()

    def _generate_company_framework(self) -> Dict:
        """
        生成企业调研框架

        Returns:
            Dict: 企业调研框架
        """
        # 确定调研来源
        has_local_docs = len(self.local_docs_content) > 0
        research_source = "本地文档" if has_local_docs else "web-search"
        
        company_info = {
            "company_name": self.company_name,
            "country": self.country,
            "research_source": research_source,
            "local_docs_count": len(self.local_docs_content),
            "research_status": f"框架已生成，待智能体通过 {research_source} 深度调研",
            "company_overview": {
                "introduction": self._get_introduction(),
                "established_year": self._get_established_year(),
                "team_size": self._get_team_size()
            },
            "business_info": {
                "main_business": self._get_main_business(),
                "business_model": self._get_business_model(),
                "core_services": self._get_core_services()
            },
            "products": {
                "core_products": self._get_core_products(),
                "product_features": self._get_product_features()
            },
            "tags": {
                "industry_tags": self._get_industry_tags(),
                "business_tags": self._get_business_tags(),
                "market_position": self._get_market_position()
            },
            "customers": {
                "main_customers": self._get_main_customers(),
                "customer_segments": self._get_customer_segments()
            },
            "local_docs_extracted": self.local_docs_content.keys() if has_local_docs else [],
            "research_queries": self._generate_research_queries(),
            "industry_research_queries": self._generate_industry_queries()
        }

        return company_info

    def _get_introduction(self) -> str:
        """从本地文档提取公司介绍"""
        if self.local_docs_content:
            info = self._extract_info_from_local_docs("公司介绍")
            if info != "未找到相关信息":
                return info[:200] + "..." if len(info) > 200 else info
            info = self._extract_info_from_local_docs("简介")
            if info != "未找到相关信息":
                return info[:200] + "..." if len(info) > 200 else info
        return f"{self.company_name} 是一家位于{self.country}的企业，具体介绍需通过深度调研获取。"

    def _get_established_year(self) -> str:
        """从本地文档提取成立年份"""
        if self.local_docs_content:
            info = self._extract_info_from_local_docs("成立")
            if info != "未找到相关信息":
                return info
        return "待调研"

    def _get_team_size(self) -> str:
        """从本地文档提取团队规模"""
        if self.local_docs_content:
            info = self._extract_info_from_local_docs("团队")
            if info != "未找到相关信息":
                return info
            info = self._extract_info_from_local_docs("员工")
            if info != "未找到相关信息":
                return info
        return "待调研"

    def _get_main_business(self) -> str:
        """从本地文档提取主营业务"""
        if self.local_docs_content:
            info = self._extract_info_from_local_docs("主营业务")
            if info != "未找到相关信息":
                return info[:200] + "..." if len(info) > 200 else info
            info = self._extract_info_from_local_docs("核心业务")
            if info != "未找到相关信息":
                return info[:200] + "..." if len(info) > 200 else info
        return "待深度调研主营业务"

    def _get_business_model(self) -> str:
        """从本地文档提取业务模式"""
        if self.local_docs_content:
            info = self._extract_info_from_local_docs("业务模式")
            if info != "未找到相关信息":
                return info
        return "待调研"

    def _get_core_services(self) -> List[str]:
        """从本地文档提取核心服务"""
        if self.local_docs_content:
            info = self._extract_info_from_local_docs("核心服务")
            if info != "未找到相关信息":
                # 简单解析列表
                lines = info.split('\n')
                services = [line.strip('-*').strip() for line in lines if line.strip()]
                return services[:5] if len(services) > 5 else services
        return ["待调研"]

    def _get_core_products(self) -> List[str]:
        """从本地文档提取核心产品"""
        if self.local_docs_content:
            info = self._extract_info_from_local_docs("核心产品")
            if info != "未找到相关信息":
                lines = info.split('\n')
                products = [line.strip('-*').strip() for line in lines if line.strip()]
                return products[:5] if len(products) > 5 else products
            info = self._extract_info_from_local_docs("产品")
            if info != "未找到相关信息":
                lines = info.split('\n')
                products = [line.strip('-*').strip() for line in lines if line.strip()]
                return products[:5] if len(products) > 5 else products
        return ["待调研"]

    def _get_product_features(self) -> str:
        """从本地文档提取产品特点"""
        if self.local_docs_content:
            info = self._extract_info_from_local_docs("产品特点")
            if info != "未找到相关信息":
                return info[:200] + "..." if len(info) > 200 else info
        return "待调研"

    def _get_industry_tags(self) -> List[str]:
        """从本地文档提取行业标签"""
        if self.local_docs_content:
            info = self._extract_info_from_local_docs("行业")
            if info != "未找到相关信息":
                return [info.strip()]
        return ["待调研"]

    def _get_business_tags(self) -> List[str]:
        """从本地文档提取业务标签"""
        if self.local_docs_content:
            info = self._extract_info_from_local_docs("业务")
            if info != "未找到相关信息":
                return [info.strip()]
        return ["待调研"]

    def _get_market_position(self) -> str:
        """从本地文档提取市场定位"""
        if self.local_docs_content:
            info = self._extract_info_from_local_docs("定位")
            if info != "未找到相关信息":
                return info
        return "待调研"

    def _get_main_customers(self) -> List[str]:
        """从本地文档提取主要客户"""
        if self.local_docs_content:
            info = self._extract_info_from_local_docs("客户")
            if info != "未找到相关信息":
                lines = info.split('\n')
                customers = [line.strip('-*').strip() for line in lines if line.strip()]
                return customers[:3] if len(customers) > 3 else customers
        return ["待调研"]

    def _get_customer_segments(self) -> str:
        """从本地文档提取客户细分"""
        if self.local_docs_content:
            info = self._extract_info_from_local_docs("客户群体")
            if info != "未找到相关信息":
                return info
        return "待调研"

    def _generate_research_queries(self) -> List[str]:
        """
        生成企业调研搜索问题清单（供智能体 web-search 使用）

        Returns:
            List[str]: 调研问题列表
        """
        return [
            f"{self.company_name} 公司介绍 成立时间 发展历程",
            f"{self.company_name} 主营业务 核心业务 服务范围",
            f"{self.company_name} 代表产品 核心产品 主要服务",
            f"{self.company_name} 行业分类 业务标签 所属行业",
            f"{self.company_name} 客户群体 主要客户 服务对象",
            f"{self.company_name} 团队规模 员工人数 组织架构",
            f"{self.company_name} 竞争优势 核心竞争力 业务特点",
            f"{self.company_name} 财务状况 营收规模（如有公开信息）"
        ]

    def _generate_industry_queries(self) -> List[Dict[str, str]]:
        """
        生成行业调研搜索问题（痛点 + 案例）

        Returns:
            List[Dict]: 行业调研问题列表，含搜索目的说明
        """
        return [
            {
                "purpose": "行业共性痛点",
                "query": f"{self.company_name} 所在行业 痛点 挑战 2024 2025",
                "collect": "行业普遍痛点、典型表现、量化数据"
            },
            {
                "purpose": "行业AI应用案例（通用）",
                "query": f"{self.company_name} 所在行业 AI应用 智能化 案例",
                "collect": "至少3个标杆企业案例：企业背景、应用场景、技术方案、实施效果"
            },
            {
                "purpose": "行业AI应用案例（细分）",
                "query": f"{self.company_name} 核心业务 AI LLM 实践",
                "collect": "细分业务领域的AI实践案例和关键成功因素"
            }
        ]

    def format_output(self, company_info: Dict, format_type: str = "markdown") -> str:
        """
        格式化输出

        Args:
            company_info: 公司信息字典
            format_type: 输出格式（markdown/json）

        Returns:
            str: 格式化输出
        """
        if format_type == "json":
            return json.dumps(company_info, ensure_ascii=False, indent=2)
        else:
            return self._format_markdown(company_info)

    def _format_markdown(self, company_info: Dict) -> str:
        """
        格式化为Markdown

        Args:
            company_info: 公司信息字典

        Returns:
            str: Markdown格式
        """
        md = f"# {company_info['company_name']} 企业调研框架\n\n"
        md += f"**调研状态**: {company_info.get('research_status', '未知')}\n\n"
        md += f"**国家/地区**: {company_info['country']}\n\n"

        # 公司概览
        md += "## 公司概览\n\n"
        overview = company_info.get('company_overview', {})
        md += f"- **公司介绍**: {overview.get('introduction', '待调研')}\n"
        md += f"- **成立年份**: {overview.get('established_year', '待调研')}\n"
        md += f"- **团队规模**: {overview.get('team_size', '待调研')}\n\n"

        # 业务信息
        md += "## 业务信息\n\n"
        business = company_info.get('business_info', {})
        md += f"- **主营业务**: {business.get('main_business', '待调研')}\n"
        md += f"- **业务模式**: {business.get('business_model', '待调研')}\n\n"

        core_services = business.get('core_services', [])
        if core_services and core_services != ["待调研"]:
            md += "**核心服务**:\n"
            for i, service in enumerate(core_services, 1):
                md += f"{i}. {service}\n"
            md += "\n"

        # 产品信息
        md += "## 产品/服务\n\n"
        products = company_info.get('products', {})
        core_products = products.get('core_products', [])
        if core_products and core_products != ["待调研"]:
            md += "**代表产品**:\n"
            for i, product in enumerate(core_products, 1):
                md += f"{i}. {product}\n"
            md += "\n"

        # 标签
        md += "## 行业/业务标签\n\n"
        tags = company_info.get('tags', {})
        industry_tags = tags.get('industry_tags', [])
        business_tags = tags.get('business_tags', [])

        if industry_tags and industry_tags != ["待调研"]:
            md += f"- **行业**: {', '.join(industry_tags)}\n"
        if business_tags and business_tags != ["待调研"]:
            md += f"- **业务**: {', '.join(business_tags)}\n"

        # 企业调研查询
        if "research_queries" in company_info:
            md += "\n## 待调研问题清单（企业信息）\n\n"
            md += "以下问题需要智能体通过 **web-search** 工具深度调研：\n\n"
            queries = company_info["research_queries"]
            for i, query in enumerate(queries, 1):
                md += f"{i}. `{query}`\n"

        # 行业调研查询
        if "industry_research_queries" in company_info:
            md += "\n## 待调研问题清单（行业信息）\n\n"
            for item in company_info["industry_research_queries"]:
                md += f"### {item['purpose']}\n"
                md += f"- **搜索关键词**: `{item['query']}`\n"
                md += f"- **收集内容**: {item['collect']}\n\n"

        return md


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='企业深度调研框架生成器 - 支持 web-search 和本地文档两种调研模式'
    )
    parser.add_argument('--company-name', required=True, help='公司名称')
    parser.add_argument('--country', default='中国', help='国家/地区（默认：中国）')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown',
                       help='输出格式（默认：markdown）')
    parser.add_argument('--local-docs-dir', help='本地Markdown文档目录路径（用于初创企业信息收集）')
    parser.add_argument('--output', '-o', help='输出文件路径（如未指定，自动保存到 output/ 目录）')
    parser.add_argument('--no-save', action='store_true', help='不保存到文件，仅输出到控制台')

    args = parser.parse_args()

    try:
        researcher = CompanyResearcher(
            company_name=args.company_name,
            country=args.country,
            local_docs_dir=args.local_docs_dir
        )

        company_info = researcher.research_company()
        output = researcher.format_output(company_info, args.format)
        
        # 输出到控制台
        print(output)
        
        # 保存到文件（除非指定 --no-save）
        if not args.no_save:
            if args.output:
                # 使用指定的输出路径
                output_path = args.output
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
            else:
                # 使用默认输出目录
                output_dir = "output"
                os.makedirs(output_dir, exist_ok=True)
                # 生成文件名：{公司名称}_调研框架.{格式}
                ext = "md" if args.format == "markdown" else "json"
                safe_company_name = args.company_name.replace('/', '_').replace('\\', '_').replace(':', '_')
                output_path = os.path.join(output_dir, f"{safe_company_name}_调研框架.{ext}")
            
            # 保存文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n[调研] 报告已保存到: {os.path.abspath(output_path)}")
            
            # 记录执行日志
            log_execution(args.company_name, output_path, args.format, args.local_docs_dir)

        return 0

    except Exception as e:
        print(f"[错误] {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
