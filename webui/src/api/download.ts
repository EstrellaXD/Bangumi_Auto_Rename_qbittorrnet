import type { BangumiAPI, BangumiRule } from '#/bangumi';
import type { RSS } from '#/rss';
import type { ApiSuccess } from '#/api';

export const apiDownload = {
  /**
   * 解析 RSS 链接
   * @param rss_item - RSS 链接
   */
  async analysis(rss_item: RSS) {
    const { data } = await axios.post<BangumiAPI>(
      'api/v1/rss/analysis',
      rss_item
    );

    const result: BangumiRule = {
      ...data,
      filter: data.filter.split(','),
      rss_link: data.rss_link.split(','),
    };
    return result;
  },

  /**
   * 旧番
   * @param bangumiData - Bangumi 数据
   */
  async collection(bangumiData: BangumiRule) {
    const postData: BangumiAPI = {
      ...bangumiData,
      filter: bangumiData.filter.join(','),
      rss_link: bangumiData.rss_link.join(','),
    };
    const { data } = await axios.post<ApiSuccess>(
      'api/v1/rss/collect',
      postData
    );
    return data;
  },

  /**
   * 新番
   * @param bangumiData - Bangumi 数据
   */
  async subscribe(bangumiData: BangumiRule, rss: RSS) {
    const bangumi: BangumiAPI = {
      ...bangumiData,
      filter: bangumiData.filter.join(','),
      rss_link: bangumiData.rss_link.join(','),
    };
    const postData = {
      data: bangumi,
      rss,
    };
    const { data } = await axios.post<ApiSuccess>(
      'api/v1/rss/subscribe',
      postData
    );
    return data;
  },
};
