#!/usr/bin/nodejs

const url = 'https://lionsclub-annweiler.de/gewinne/';
const configfile = 'config.yaml'

const request = require('request');
const jsdom = require('jsdom');
const yaml = require('js-yaml');
const fs = require('fs');

function main() {
  request(url, (error, response, body) => {
    getData(body);
  });
}

function readConfig() {
  try {
    return yaml.safeLoad(fs.readFileSync(configfile, 'utf8'));
  } catch (e) {
    console.log(e);
  }
}

function getData(html) {
  const { JSDOM } = jsdom;
  const dom = new JSDOM(html);
  const $ = (require('jquery'))(dom.window);
  const config = readConfig();

  $('.tag').each(function(index, tag) {
    t = $(tag);

    date = t.find('h3').first().html();
  
    Object.keys(config).forEach(function(key, index_key) {
      
      t.find('.line').each(function(index_line, line) {
        l = $(line);
  
        if (l.prev().find('a').html() == undefined) {
          if (l.prev().find('h3').html() != undefined) {
            supporter = l.prev().find('h3').html();
          }
        } else {
          supporter = l.prev().find('a').html();
        }
  
        article = l.find('.artikel').html();
        numbers = l.find('.losnr').html().split(', ');
  
        (numbers.includes(key)) ? console.log(date + ' ' + config[key]['name'] + ' ' + supporter + ' ' + article + ' ' + key) : undefined;
      });
    });
  });
}

main();